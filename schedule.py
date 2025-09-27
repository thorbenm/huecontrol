#!/usr/bin/python3
import re
import datetime
from personal_data import calendar_url
import sys
from systemd import journal
import scene
sys.path.insert(1, '/home/pi/Programming/frame')
from _calendar import get_events


ALLOWED_MODULES = ["scene", "wakeup", "wait_until_on"]


def split_commands(command):
    split_pattern = ['&&', ';']
    regex_split_pattern = '|'.join(map(re.escape, split_pattern))
    ret = re.split(regex_split_pattern, command)
    ret = [r.strip() for r in ret]
    return ret


def run_command(command):
    for c in split_commands(command):
        if not is_variable_definition(c):
            module = c.split()[0]
            if module not in ALLOWED_MODULES:
                raise RuntimeError(module + ' is not an allowed module')

            module = __import__(module)
            module_main = getattr(module, "main")

            module_main(c)


def is_now(dt):
    now = datetime.datetime.now()
    return (now.year == dt.year and
            now.month == dt.month and
            now.day == dt.day and
            now.hour == dt.hour and
            now.minute == dt.minute)


def get_calendar_events():
    threshold = datetime.datetime.now() - datetime.timedelta(days=7)
    return get_events(calendar_url, threshold=threshold, bunch_reoccuring=False)


def run_current_commands():
    events = get_calendar_events()
    for e in events:
        if is_now(e.start):
            c = e.name
            journal.write("schedule: " + c)
            run_command(c)


def is_variable_definition(command):
    return "=" in command


def variable_definition_command_filter(command):
    if command.startswith("scene "):
        args = scene.parse_args(command)
        if args.update:
            return f"scheduled_scene = '{args.scene}'"
    return command


def get_scene_args(command):
    if command.startswith("scene "):
        args = scene.parse_args(command)
        return args
    return None


def get_variable_definitions(break_function=lambda _: None):
    events = get_calendar_events()
    data = list()
    for e in events:
        command = e.name
        for c in split_commands(command):
            cf = variable_definition_command_filter(c)
            if is_variable_definition(cf):
                variable = cf.split("=")[0].strip()
                value = eval(cf.split("=")[1].strip())

                element = lambda: None
                element.when = e.start
                element.variable = variable
                element.value = value
                element.scene_args = get_scene_args(c)

                if break_function(element):
                    return data

                data.append(element)
    return data


def get_variable(name, hour=None, minute=None, dt=None):
    if dt is None:
        dt = datetime.datetime.now()
    dt = dt.replace(second=0, microsecond=0)
    if hour is not None:
        dt = dt.replace(hour=hour)
    if minute is not None:
        dt = dt.replace(minute=minute)

    data = get_variable_definitions()
    data = [d for d in data if d.when <= dt]
    data = [d for d in data if d.variable == name]
    return data[-1].value


def test():
    assert get_variable("auto_ct", 11, 59) == False
    assert get_variable("auto_ct", 12, 00) == True
    assert get_variable("auto_ct", 16, 59) == True
    assert get_variable("auto_ct", 17, 00) == False

    assert get_variable("scheduled_scene", 6, 59) == "gemutlich"
    assert get_variable("scheduled_scene", 7, 00) == "hell"
    assert get_variable("scheduled_scene", 16, 59) == "hell"
    assert get_variable("scheduled_scene", 17, 00) == "warm"
    assert get_variable("scheduled_scene", 18, 29) == "warm"
    assert get_variable("scheduled_scene", 18, 30) == "gemutlich"
    print("all tests passed")


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "update":
        force_update_buffered()
    else:
        run_current_commands()


def force_update_buffered():
    threshold = datetime.datetime.now() - datetime.timedelta(days=7)
    get_events(calendar_url, threshold=threshold, bunch_reoccuring=False,
               refresh_interval_minutes=-1)


if __name__ == '__main__':
    main()
