#!/usr/bin/python3
import _phue
import time
import argparse


def parse_args(input_args=None):
    if isinstance(input_args, str):
        input_args = input_args.split()
        this_file = __file__.split("/")[-1].removesuffix(".py")
        if input_args[0].startswith(this_file):
            input_args = input_args[1:]

    parser = argparse.ArgumentParser()
    parser.add_argument('light', type=str)
    args = parser.parse_args(input_args if input_args else None)

    return args


def main(input_args=None):
    args = parse_args(input_args)
    while not _phue.get_on(args.light):
        time.sleep(10.0)


if __name__ == '__main__':
    main()
