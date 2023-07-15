#!/usr/bin/python3
import sys
from time import sleep
import _phue
import argparse
import scene


def wakeup(t1, t2, t3, t4):
    scene.min_schlafzimmer(increase_only=True)
    scene.min_wohnzimmer(increase_only=True)

    sleep(t1 + .1)

    if _phue.is_on("Nachttischlampe"):
        scene.lesen_schlafzimmer(t2, increase_only=True)
    if _phue.is_on("Stehlampe"):
        scene.lesen_wohnzimmer(t2, increase_only=True)

    sleep(t2 + .1)

    if _phue.is_on("Nachttischlampe"):
        scene.hell_schlafzimmer(t3, increase_only=True)
    if _phue.is_on("Stehlampe"):
        scene.hell_wohnzimmer(t3, increase_only=True)

    if 0.0 < t4:
        sleep(t2 + .1)
        if _phue.is_on("Nachttischlampe"):
            scene.focus_schlafzimmer(t3, increase_only=True)
        if _phue.is_on("Stehlampe"):
            scene.focus_wohnzimmer(t3, increase_only=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t1', type=str, default='10m', dest='t1')
    parser.add_argument('-t2', type=str, default='3m', dest='t2')
    parser.add_argument('-t3', type=str, default='45m', dest='t3')
    parser.add_argument('-t4', type=str, default='-1s', dest='t4')
    parser.add_argument('-c', action='store_true', dest='scheduled')
    args = parser.parse_args()

    t1 = args.t1
    t2 = args.t2
    t3 = args.t3
    t4 = args.t4

    t1 = scene.convert_time_string(t1)
    t2 = scene.convert_time_string(t2)
    t3 = scene.convert_time_string(t3)
    t4 = scene.convert_time_string(t4)

    if args.scheduled:
        with open("/home/pi/scheduled_scene", "w") as file:
            file.write("hell\n")

    wakeup(t1, t2, t3, t4)


if __name__ == '__main__':
    main()
