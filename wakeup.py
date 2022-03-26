#!/usr/bin/python3
import sys
from time import sleep
import _phue
import argparse
import scene


def wakeup(t1, t2, t3):
    scene.min_schlafzimmer(increase_only=True)
    scene.min(increase_only=True)

    sleep(t1 + .1)

    if _phue.is_on("Nachttischlampe"):
        scene.gemutlich_schlafzimmer(t2, increase_only=True)
    if _phue.is_on("Stehlampe"):
        scene.gemutlich(t2, increase_only=True)

    sleep(t2 + .1)

    if _phue.is_on("Nachttischlampe"):
        scene.hell_schlafzimmer(t3, increase_only=True)
    if _phue.is_on("Stehlampe"):
        scene.hell(t3, increase_only=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--fast', action='store_true', dest='fast')
    parser.add_argument('-s', '--slow', action='store_true', dest='slow')
    parser.add_argument('-t1', type=str, default='10m', dest='t1')
    parser.add_argument('-t2', type=str, default='3m', dest='t2')
    parser.add_argument('-t3', type=str, default='45m', dest='t3')
    args = parser.parse_args()

    if args.fast:
        t1 = "10m"
        t2 = "3m"
        t3 = "45m"
    elif args.slow:
        t1 = "15m"
        t2 = "15m"
        t3 = "45m"
    else:
        t1 = args.t1
        t2 = args.t2
        t3 = args.t3

    t1 = scene.convert_time_string(t1)
    t2 = scene.convert_time_string(t2)
    t3 = scene.convert_time_string(t3)

    wakeup(t1, t2, t3)


if __name__ == '__main__':
    main()
