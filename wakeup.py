#!/usr/bin/python3
import sys
from time import sleep
import _phue
import argparse
import scene
import ambient
import toolbox
import data


def wakeup(t1, t2, t3, t4, schlafzimmer, wohnzimmer):
    s1 = "min"
    if schlafzimmer:
        scene.transition(s1 + "_schlafzimmer", increase_only=True)
    if wohnzimmer:
        scene.transition(s1 + "_wohnzimmer", increase_only=True)
    sleep(t1 + .1)

    s2 = "gemutlich"
    if _phue.get_on("Nachttischlampe") and schlafzimmer:
        scene.transition(s2 + "_schlafzimmer", time=t2, increase_only=True)
    if _phue.get_on("Stehlampe") and wohnzimmer:
        scene.transition(s2 + "_wohnzimmer", time=t2, increase_only=True)
    sleep(t2 + .1)

    s3 = "halbwarm"
    if _phue.get_on("Nachttischlampe") and schlafzimmer:
        scene.transition(s3 + "_schlafzimmer", time=t3, increase_only=True)
    if _phue.get_on("Stehlampe") and wohnzimmer:
        scene.transition(s3 + "_wohnzimmer", time=t3, increase_only=True)
    sleep(t3 + .1)

    s4 = "hell"
    if _phue.get_on("Nachttischlampe") and schlafzimmer:
        scene.transition(s4 + "_schlafzimmer", time=t4, increase_only=True)
    if _phue.get_on("Stehlampe") and wohnzimmer:
        scene.transition(s4 + "_wohnzimmer", time=t4, increase_only=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t1', type=str, default='1s', dest='t1')
    parser.add_argument('-t2', type=str, default='auto', dest='t2')
    parser.add_argument('-t3', type=str, default='2m', dest='t3')
    parser.add_argument('-t4', type=str, default='auto', dest='t4')
    parser.add_argument('-c', action='store_true', dest='scheduled')
    parser.add_argument('-w', action='store_true', dest='wohnzimmer')
    parser.add_argument('-s', action='store_true', dest='schlafzimmer')
    args = parser.parse_args()

    t1 = args.t1
    t2 = args.t2
    t3 = args.t3
    t4 = args.t4

    t1 = toolbox.convert_time_string(t1)

    if t2 == "auto":
        if _phue.get_on("Nachttischlampe") or _phue.get_on("Stehlampe"):
            t2 = "1m"
        else:
            t2 = "10m"
    t2 = toolbox.convert_time_string(t2)

    t3 = toolbox.convert_time_string(t3)

    if t4 == "auto":
        t4 = toolbox.map(ambient.get_simulated_bri() ** .5, 0, 1, 90 * 60, 5 * 60)
    else:
        t4 = toolbox.convert_time_string(t4)

    if args.scheduled:
        with open("/home/pi/scheduled_scene", "w") as file:
            file.write("hell\n")

    wakeup(t1, t2, t3, t4, args.schlafzimmer, args.wohnzimmer)


if __name__ == '__main__':
    main()
