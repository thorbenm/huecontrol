#!/usr/bin/python3
import sys
from time import sleep
import _phue
import argparse
import scene
import ambient
import toolbox
import data


def wakeup(t1, t2, t3, t4, rooms):
    master = dict()
    master["schlafzimmer"] = data.get_lights("schlafzimmer")[0]
    master["wohnzimmer"] = data.get_lights("wohnzimmer")[0]
    master["kinderzimmer"] = data.get_lights("kinderzimmer")[0]

    if "schlafzimmer" in rooms:
        override_attributes = data.get_scene("min")[master["schlafzimmer"]]
        scene.transition(name="off", room="schlafzimmer", increase_only=True,
                         _override={master["schlafzimmer"]: override_attributes})
    if "wohnzimmer" in rooms:
        scene.transition(name="min", room="wohnzimmer", increase_only=True)
    if "kinderzimmer" in rooms:
        scene.transition(name="min", room="kinderzimmer", increase_only=True)

    sleep(t1 + .1)

    s2 = "gemutlich"
    if "schlafzimmer" in rooms and _phue.get_on(master["schlafzimmer"]):
        override_attributes = data.get_scene(s2)[master["schlafzimmer"]]
        scene.transition(name="off", room="schlafzimmer", time=t2, increase_only=True,
                         _override={master["schlafzimmer"]: override_attributes})
    if "wohnzimmer" in rooms and _phue.get_on(master["wohnzimmer"]):
        scene.transition(name=s2, room="wohnzimmer", time=t2, increase_only=True,
                         _override={"Lichterkette": {"on": False}})
    if "kinderzimmer" in rooms and _phue.get_on(master["kinderzimmer"]):
        scene.transition(name=s2, room="kinderzimmer", time=t2, increase_only=True)

    sleep(t2 + .1)

    s3 = "halbwarm"
    if "schlafzimmer" in rooms and _phue.get_on(master["schlafzimmer"]):
        scene.transition(name=s3, room="schlafzimmer", time=t3, increase_only=True)
    if "wohnzimmer" in rooms and _phue.get_on(master["wohnzimmer"]):
        scene.transition(name=s3, room="wohnzimmer", time=t3, increase_only=True,
                         _override={"Lichterkette": {"on": False}})
    if "kinderzimmer" in rooms and _phue.get_on(master["kinderzimmer"]):
        scene.transition(name=s3, room="kinderzimmer", time=t3, increase_only=True)

    sleep(t3 + .1)

    s4 = "hell"
    if "schlafzimmer" in rooms and _phue.get_on(master["schlafzimmer"]):
        scene.transition(name=s4, room="schlafzimmer", time=t4, increase_only=True)
    if "wohnzimmer" in rooms and _phue.get_on(master["wohnzimmer"]):
        scene.transition(name=s4, room="wohnzimmer", time=t4, increase_only=True)
    if "kinderzimmer" in rooms and _phue.get_on(master["kinderzimmer"]):
        scene.transition(name=s4, room="kinderzimmer", time=t4, increase_only=True)


def parse_args(input_args=None):
    if isinstance(input_args, str):
        input_args = input_args.split()
        this_file = __file__.split("/")[-1].removesuffix(".py")
        if input_args[0].startswith(this_file):
            input_args = input_args[1:]

    parser = argparse.ArgumentParser()
    parser.add_argument('-t1', type=str, default='1s', dest='t1')
    parser.add_argument('-t2', type=str, default='10m', dest='t2')
    parser.add_argument('-t3', type=str, default='5m', dest='t3')
    parser.add_argument('-t4', type=str, default='auto', dest='t4')
    parser.add_argument('-c', action='store_true', dest='scheduled')
    parser.add_argument('-w', action='store_true', dest='wohnzimmer')
    parser.add_argument('-s', action='store_true', dest='schlafzimmer')
    parser.add_argument('-k', action='store_true', dest='kinderzimmer')
    args = parser.parse_args(input_args if input_args else None)

    if not args.wohnzimmer and not args.schlafzimmer and not args.kinderzimmer:
        args.wohnzimmer = True
        args.schlafzimmer = True
        args.kinderzimmer = True

    args.t1 = toolbox.convert_time_string(args.t1)
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

    rooms = []
    if args.schlafzimmer:
        rooms.append("schlafzimmer")
    if args.wohnzimmer:
        rooms.append("wohnzimmer")
    if args.kinderzimmer:
        rooms.append("kinderzimmer")

    wakeup(args.t1, args.t2, args.t3, args.t4, rooms)


if __name__ == '__main__':
    main()
