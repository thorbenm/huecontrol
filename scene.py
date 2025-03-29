#!/usr/bin/python3
import os
from _phue import set_lights
import argparse
import data
import toolbox
from time import time as now


def find_duplicate_values(dictionary):
    values_to_keys = {}
    result_keys = []
    result_values = []

    for key, value in dictionary.items():
        value_str = str(value)
        if value_str in values_to_keys:
            index = values_to_keys[value_str]
            result_keys[index].append(key)
        else:
            values_to_keys[value_str] = len(result_keys)
            result_keys.append([key])
            result_values.append(value)

    return result_keys, result_values


def transition_dicionary(d, time=.4, reduce_only=False, increase_only=False):
    keys, values = find_duplicate_values(d)
    for k, v in zip(keys, values):
        set_lights(k, **v, time=time, reduce_only=reduce_only,
                   increase_only=increase_only)


TRANSITION_FILE = "/home/pi/transition"


def transition(name, room="all", time=.4, reduce_only=False, increase_only=False,
               low_priority=False, abort_wakeup=True, _override={}):
    if room == "all":
        rooms = data.get_rooms()
    else:
        rooms = [room]

    if low_priority:
        for r in rooms:
            if transition_in_progress(r):
                rooms.remove(r)

    if abort_wakeup:
        for r in rooms:
            path = "/home/pi/wakeup_in_progress" + "_" + r
            if os.path.exists(path):
                os.remove(path)

    d = {}
    for r in rooms:
        d = {**d, **data.get_scene(name, r)}

    d = {**d, **_override}
    transition_dicionary(d, time=time, reduce_only=reduce_only,
                         increase_only=increase_only)

    if 1.0 < time:
        transition_end = now() + time
        for r in rooms:
            with open(TRANSITION_FILE + "_" + r, "w") as f:
                f.write(str(transition_end))
    else:
        for r in rooms:
            if os.path.exists(TRANSITION_FILE + "_" + r):
                os.remove(TRANSITION_FILE + "_" + r)

    return d


def transition_in_progress(room):
    if room not in data.get_rooms():
        raise ValueError(f"Room {room} not found")

    file_name = TRANSITION_FILE + "_" + room
    if os.path.exists(file_name):
        with open(file_name, "r") as f:
            ret = now() < float(f.read())
            if not ret:
                os.remove(file_name)
            return ret
    return False


def parse_args(input_args=None):
    if isinstance(input_args, str):
        input_args = input_args.split()
        this_file = __file__.split("/")[-1].removesuffix(".py")
        if input_args[0].startswith(this_file):
            input_args = input_args[1:]

    parser = argparse.ArgumentParser()
    parser.add_argument(type=str, dest='scene')
    parser.add_argument(type=str, dest='room', default="all", nargs='?')
    parser.add_argument('-t', type=str, default='0.4s', dest='time')
    parser.add_argument('-r', '--reduce-only', action='store_true', dest='reduce_only')
    parser.add_argument('-w', action='store_true', dest='write_scheduled',
                        help='store as scheduled scene')
    parser.add_argument('-l', action='store_true', dest='low_priority',
                        help='will not abort ongoing transition')
    args = parser.parse_args(input_args if input_args else None)

    args.time = toolbox.convert_time_string(args.time)
    return args


def main(input_args=None):
    args = parse_args(input_args)
    transition(name=args.scene, room=args.room, time=args.time,
               reduce_only=args.reduce_only, low_priority=args.low_priority)


if __name__ == '__main__':
    main()
