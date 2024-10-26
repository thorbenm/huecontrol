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
    if schlafzimmer:
        scene.transition("nachtlicht_schlafzimmer", increase_only=True)
    if wohnzimmer:
        scene.transition("min_wohnzimmer", increase_only=True)
    sleep(t1 + .1)

    s2 = "gemutlich"
    if _phue.get_on("Wickeltischlampe") and schlafzimmer:  # different lamp !!!
        _phue.set_lights("Wickeltischlampe", **getattr(data, "warm")["Wickeltischlampe"], time=t2, increase_only=True)  # not consistent
    if _phue.get_on("Stehlampe") and wohnzimmer:
        scene.transition(s2 + "_wohnzimmer", time=t2, increase_only=True, _override={"Lichterkette": {"on": False}})
    sleep(t2 + .1)

    s3 = "halbwarm"
    if _phue.get_on("Wickeltischlampe") and schlafzimmer:  # different lamp!!!
        scene.transition(s3 + "_schlafzimmer", time=t3, increase_only=True)
    if _phue.get_on("Stehlampe") and wohnzimmer:
        scene.transition(s3 + "_wohnzimmer", time=t3, increase_only=True, _override={"Lichterkette": {"on": False}})
    sleep(t3 + .1)

    s4 = "hell"
    if _phue.get_on("Nachttischlampe") and schlafzimmer and getattr(data, s3)["Nachttischlampe"]["ct"] - 0.02 < _phue.get_ct("Nachttischlampe"):
        scene.transition(s4 + "_schlafzimmer", time=t4, increase_only=True)
    if _phue.get_on("Stehlampe") and wohnzimmer and getattr(data, s3)["Stehlampe"]["ct"] - 0.02 < _phue.get_ct("Stehlampe"):
        scene.transition(s4 + "_wohnzimmer", time=t4, increase_only=True)


def parse_args(input_args=None):
    if isinstance(input_args, str):
        input_args = input_args.split()
        this_file = __file__.split("/")[-1].removesuffix(".py")
        if input_args[0].startswith(this_file):
            input_args = input_args[1:]

    parser = argparse.ArgumentParser()
    parser.add_argument('-t1', type=str, default='1s', dest='t1')
    parser.add_argument('-t2', type=str, default='auto', dest='t2')
    parser.add_argument('-t3', type=str, default='3m', dest='t3')
    parser.add_argument('-t4', type=str, default='auto', dest='t4')
    parser.add_argument('-c', action='store_true', dest='scheduled')
    parser.add_argument('-w', action='store_true', dest='wohnzimmer')
    parser.add_argument('-s', action='store_true', dest='schlafzimmer')
    args = parser.parse_args(input_args if input_args else None)

    if not args.wohnzimmer and not args.schlafzimmer:
        args.wohnzimmer = True
        args.schlafzimmer = True

    args.t1 = toolbox.convert_time_string(args.t1)

    if args.t2 == "auto":
        if _phue.get_on("Nachttischlampe") or _phue.get_on("Stehlampe"):
            args.t2 = "3m"
        else:
            args.t2 = "10m"
    args.t2 = toolbox.convert_time_string(args.t2)
    args.t3 = toolbox.convert_time_string(args.t3)

    if args.t4 == "auto":
        args.t4 = toolbox.map(ambient.get_simulated_bri(), 0, .5, 90 * 60, 5 * 60, clamp=True)
    else:
        args.t4 = toolbox.convert_time_string(args.t4)

    return args


def main(input_args=None):
    args = parse_args(input_args)
    if args.scheduled:
        with open("/home/pi/scheduled_scene", "w") as file:
            file.write("hell\n")

    wakeup(args.t1, args.t2, args.t3, args.t4, args.schlafzimmer, args.wohnzimmer)


if __name__ == '__main__':
    main()
