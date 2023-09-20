#!/usr/bin/python3
import sys
from time import sleep
import _phue
import argparse
import scene


def wakeup(t1, t2, t3, t4, schlafzimmer, wohnzimmer, schlafzimmer_h, wohnzimmer_h):
    if schlafzimmer:
        scene.transition("min_schlafzimmer", increase_only=True)
    if wohnzimmer:
        scene.transition("min_wohnzimmer", increase_only=True)

    sleep(t1 + .1)

    if _phue.is_on("Nachttischlampe") and schlafzimmer:
        scene.transition("warm_schlafzimmer", time=t2, increase_only=True)
    if _phue.is_on("Stehlampe") and wohnzimmer:
        scene.transition("warm_wohnzimmer", time=t2, increase_only=True)

    sleep(t2 + .1)

    if _phue.is_on("Nachttischlampe") and schlafzimmer:
        override = {}
        if not schlafzimmer_h:
            override = {"Schlafzimmer Hängelampe": {'on': False}}
        scene.transition("hell_schlafzimmer", time=t3, increase_only=True,
                         _override=override)
    if _phue.is_on("Stehlampe") and wohnzimmer:
        override = {}
        if not wohnzimmer_h:
            override = {"Hängelampe": {'on': False}}
        scene.transition("hell_wohnzimmer", time=t3, increase_only=True,
                         _override=override)

    if 0.0 < t4:
        sleep(t2 + .1)
        if _phue.is_on("Nachttischlampe") and schlafzimmer:
            scene.transition("focus_schlafzimmer", time=t4, increase_only=True)
        if _phue.is_on("Stehlampe") and wohnzimmer:
            scene.transition("focus_wohnzimmer", time=t4, increase_only=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t1', type=str, default='1s', dest='t1')
    parser.add_argument('-t2', type=str, default='15m', dest='t2')
    parser.add_argument('-t3', type=str, default='45m', dest='t3')
    parser.add_argument('-t4', type=str, default='-1s', dest='t4')
    parser.add_argument('-c', action='store_true', dest='scheduled')
    parser.add_argument('-w', action='store_true', dest='wohnzimmer')
    parser.add_argument('-s', action='store_true', dest='schlafzimmer')
    parser.add_argument('-wh', action='store_true', dest='wohnzimmer_h')
    parser.add_argument('-sh', action='store_true', dest='schlafzimmer_h')
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

    wakeup(t1, t2, t3, t4, args.schlafzimmer, args.wohnzimmer,
           args.schlafzimmer_h, args.wohnzimmer_h)


if __name__ == '__main__':
    main()
