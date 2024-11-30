#!/usr/bin/python3
from _phue import set_lights
import argparse
import data
import toolbox


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


def transition(name, room="all", time=.4, reduce_only=False, increase_only=False,
              _override={}):
    d = data.get_scene(name, room)
    d = {**d, **_override}
    transition_dicionary(d, time=time, reduce_only=reduce_only,
                         increase_only=increase_only)


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
    args = parser.parse_args(input_args if input_args else None)

    args.time = toolbox.convert_time_string(args.time)
    return args


def main(input_args=None):
    args = parse_args(input_args)
    transition(name=args.scene, room=args.room, time=args.time,
               reduce_only=args.reduce_only)


if __name__ == '__main__':
    main()
