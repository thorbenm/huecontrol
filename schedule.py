#!/usr/bin/python3
import re
import datetime
from personal_data import calendar_url
import sys
from systemd import journal
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
        module = c.split()[0]
        if module not in ALLOWED_MODULES:
            raise RuntimeError(module + ' is not an allowed module')

        module = __import__(module)
        module_main = getattr(module, "main")
        module_parse_args = getattr(module, "parse_args")

        module_main(c)


def is_now(dt):
    now = datetime.datetime.now()
    return (now.year == dt.year and
            now.month == dt.month and
            now.day == dt.day and
            now.hour == dt.hour and
            now.minute == dt.minute)


def run_current_commands():
    events = get_events(calendar_url, threshold=(datetime.datetime.now()-datetime.timedelta(days=7)), bunch_reoccuring=False)
    for e in events:
        if is_now(e.start):
            c = e.name
            journal.write("schedule: " + c)
            run_command(c)


def main():
    run_current_commands()


if __name__ == '__main__':
    main()
