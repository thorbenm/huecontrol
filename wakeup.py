#!/usr/bin/python3
import sys
from time import sleep
import _phue
import argparse
import scene
import ambient
import toolbox


def wakeup(t1, t2, t3, schlafzimmer, wohnzimmer):
    if schlafzimmer:
        scene.transition("min_schlafzimmer", increase_only=True)
    if wohnzimmer:
        scene.transition("min_wohnzimmer", increase_only=True)

    sleep(t1 + .1)

    if _phue.get_on("Nachttischlampe") and schlafzimmer:
        scene.transition("warm_schlafzimmer", time=t2, increase_only=True)
    if _phue.get_on("Stehlampe") and wohnzimmer:
        scene.transition("warm_wohnzimmer", time=t2, increase_only=True)

    sleep(t2 + .1)

    if _phue.get_on("Nachttischlampe") and schlafzimmer:
        scene.transition("hell_schlafzimmer", time=t3, increase_only=True)
    if _phue.get_on("Stehlampe") and wohnzimmer:
        scene.transition("hell_wohnzimmer", time=t3, increase_only=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t1', type=str, default='1s', dest='t1')
    parser.add_argument('-t2', type=str, default='10m', dest='t2')
    parser.add_argument('-t3', type=str, default='auto', dest='t3')
    parser.add_argument('-c', action='store_true', dest='scheduled')
    parser.add_argument('-w', action='store_true', dest='wohnzimmer')
    parser.add_argument('-s', action='store_true', dest='schlafzimmer')
    args = parser.parse_args()

    t1 = args.t1
    t2 = args.t2
    t3 = args.t3

    t1 = toolbox.convert_time_string(t1)
    t2 = toolbox.convert_time_string(t2)
    if t3 == "auto":
        t3 = toolbox.map(ambient.get_simulated_bri(), 0, 1, 90 * 60, 5 * 60)
    else:
        t3 = toolbox.convert_time_string(t3)

    if args.scheduled:
        with open("/home/pi/scheduled_scene", "w") as file:
            file.write("hell\n")

    wakeup(t1, t2, t3, args.schlafzimmer, args.wohnzimmer)


if __name__ == '__main__':
    main()
