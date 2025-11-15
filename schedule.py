#!/usr/bin/python3
import re
import datetime
from personal_data import calendar_url
import sys
from systemd import journal
import scene
sys.path.insert(1, '/home/pi/Programming/frame')
from _calendar import get_events
import time


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


def apply_duration_variable(events):
    pattern = '$d'
    for e in events:
        if pattern in e.name:
            duration = max(int((e.end - e.start).total_seconds()) - 60, 1)
            e.name = e.name.replace(pattern, str(duration))
    return events


def get_calendar_events():
    begin = datetime.datetime.now() - datetime.timedelta(days=2)
    end = datetime.datetime.now() + datetime.timedelta(days=2)

    events = get_events(calendar_url, threshold=begin, bunch_reoccuring=False)
    events = [e for e in events if e.start <= end]
    return apply_duration_variable(events)


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


def get_variable_definitions():
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
    s = time.time()
    assert get_variable("scheduled_scene", 5, 00) == "halbwarm"
    print(time.time() - s)

    s = time.time()
    assert get_variable("scheduled_scene", 19, 30) == "gemutlich"
    print(time.time() - s)

    print("all tests passed")


def print_events():
    for j in get_calendar_events():
        print("name", j.name, "start", j.start, "end", j.end)


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "print":
        print_events()
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
