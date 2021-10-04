#!/usr/bin/python3
import sys
from time import sleep
import _phue
import argparse
import scene


def wakeup(t1, t2, t3):
    ignore_schlafzimmer = False
    ignore_wohnzimmer = 0.9 < _phue.get_bri("Stehlampe")

    if not ignore_schlafzimmer:
        scene.gemutlich_schlafzimmer(time=.4, bri=_phue.min_bri())
    if not ignore_wohnzimmer:
        scene.gemutlich(time=.4, bri=_phue.min_bri())

    sleep(t1 + 1.0)

    if not ignore_schlafzimmer and _phue.is_on("Tischlampe"):
        scene.gemutlich_schlafzimmer(t2)
    if not ignore_wohnzimmer and _phue.is_on("Stehlampe"):
        scene.gemutlich(t2)

    sleep(t2 + 1.0)

    if not ignore_schlafzimmer and _phue.is_on("Tischlampe"):
        _phue.set_lights(["Schlafzimmer Hängelampe"], bri=_phue.min_bri())
        sleep(1.0)
        scene.hell_schlafzimmer(t3)
    if not ignore_wohnzimmer and _phue.is_on("Stehlampe"):
        _phue.set_lights(["Hängelampe"], bri=_phue.min_bri())
        sleep(1.0)
        scene.hell(t3)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t1', type=str, default='5m', dest='t1')
    parser.add_argument('-t2', type=str, default='5m', dest='t2')
    parser.add_argument('-t3', type=str, default='30m', dest='t3')
    args = parser.parse_args()

    t1 = scene.convert_time_string(args.t1)
    t2 = scene.convert_time_string(args.t2)
    t3 = scene.convert_time_string(args.t3)

    wakeup(t1, t2, t3)


if __name__ == '__main__':
    main()
