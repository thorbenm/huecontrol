#!/usr/bin/python3
import sys
from time import sleep
from _phue import set_lights
from _phue import is_on
from _phue import get_bri
from _phue import min_bri
import argparse
import motionsensor


def __wohnzimmer_prototype(bri, bri_h, ct, time, reduce_only, increase_only):
    if 90 < time:
        motionsensor.freeze()
    set_lights(["Hue Go", "Stehlampe", "Fensterlampe", "LED Streifen", "Ananas"],
               bri=bri, ct=ct, time=time, reduce_only=reduce_only, increase_only=increase_only)
    set_lights(["Hängelampe"], bri=bri_h, time=time, reduce_only=reduce_only, increase_only=increase_only)
    set_lights(["Lichterkette"], on=(min_bri() < bri), time=time, reduce_only=reduce_only, increase_only=increase_only)


def __schlafzimmer_prototype(bri, bri_h, ct, time, reduce_only, increase_only):
    set_lights(["Nachttischlampe"], bri=bri, ct=ct, time=time, reduce_only=reduce_only, increase_only=increase_only)
    set_lights(["Schlafzimmer Hängelampe"], bri=bri_h, time=time, reduce_only=reduce_only, increase_only=increase_only)


def focus(time=.4, reduce_only=False, increase_only=False):
    __wohnzimmer_prototype(bri=1.0, bri_h=1.0, ct=0, time=time, reduce_only=reduce_only, increase_only=increase_only)


def focus_schlafzimmer(time=.4, reduce_only=False, increase_only=False):
    __schlafzimmer_prototype(bri=1.0, bri_h=1.0, ct=0, time=time, reduce_only=reduce_only, increase_only=increase_only)


def hell(time=.4, reduce_only=False, increase_only=False):
    __wohnzimmer_prototype(bri=1.0, bri_h=1.0, ct=.5, time=time, reduce_only=reduce_only, increase_only=increase_only)


def hell_schlafzimmer(time=.4, reduce_only=False, increase_only=False):
    __schlafzimmer_prototype(bri=1.0, bri_h=1.0, ct=.5, time=time, reduce_only=reduce_only, increase_only=increase_only)


def warm(time=.4, reduce_only=False, increase_only=False):
    __wohnzimmer_prototype(bri=1.0, bri_h=.3, ct=1.0, time=time, reduce_only=reduce_only, increase_only=increase_only)


def warm_schlafzimmer(time=.4, reduce_only=False, increase_only=False):
    __schlafzimmer_prototype(bri=1.0, bri_h=.3, ct=1.0, time=time, reduce_only=reduce_only, increase_only=increase_only)


def lesen(time=.4, reduce_only=False, increase_only=False):
    __wohnzimmer_prototype(bri=.75, bri_h=0, ct=1.0, time=time, reduce_only=reduce_only, increase_only=increase_only)


def lesen_schlafzimmer(time=.4, reduce_only=False, increase_only=False):
    __schlafzimmer_prototype(bri=.75, bri_h=0, ct=1.0, time=time, reduce_only=reduce_only, increase_only=increase_only)


def gemutlich(time=.4, reduce_only=False, increase_only=False):
    __wohnzimmer_prototype(bri=.4, bri_h=0, ct=1.0, time=time, reduce_only=reduce_only, increase_only=increase_only)


def gemutlich_schlafzimmer(time=.4, reduce_only=False, increase_only=False):
    __schlafzimmer_prototype(bri=.4, bri_h=0, ct=1.0, time=time, reduce_only=reduce_only, increase_only=increase_only)


def dunkel(time=.4, reduce_only=False, increase_only=False):
    __wohnzimmer_prototype(bri=.1, bri_h=0, ct=1.0, time=time, reduce_only=reduce_only, increase_only=increase_only)


def dunkel_schlafzimmer(time=.4, reduce_only=False, increase_only=False):
    __schlafzimmer_prototype(bri=.1, bri_h=0, ct=1.0, time=time, reduce_only=reduce_only, increase_only=increase_only)


def min(time=.4, reduce_only=False, increase_only=False):
    __wohnzimmer_prototype(bri=min_bri(), bri_h=0, ct=1.0, time=time, reduce_only=reduce_only, increase_only=increase_only)


def min_schlafzimmer(time=.4, reduce_only=False, increase_only=False):
    __schlafzimmer_prototype(bri=min_bri(), bri_h=0, ct=1.0, time=time, reduce_only=reduce_only, increase_only=increase_only)


def off(time=.4, reduce_only=False, increase_only=False):
    __wohnzimmer_prototype(bri=0, bri_h=0, ct=1.0, time=time, reduce_only=reduce_only, increase_only=increase_only)


def off_schlafzimmer(time=.4, reduce_only=False, increase_only=False):
    __schlafzimmer_prototype(bri=0, bri_h=0, ct=1.0, time=time, reduce_only=reduce_only, increase_only=increase_only)


def convert_time_string(time_str):
    unit_is_minutes = False
    if time_str.endswith("m"):
        unit_is_minutes = True
    time = float(time_str[:-1])
    if unit_is_minutes:
        time *= 60
    return time


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', type=str, required=True, dest='scene')
    parser.add_argument('-t', type=str, default='0.4s', dest='time')
    parser.add_argument('--reduce-only', action='store_true', dest='reduce_only')
    args = parser.parse_args()

    time = convert_time_string(args.time)

    exec("%s(%f, reduce_only=%s)" % (args.scene, time, "True" if args.reduce_only else "False"))


if __name__ == '__main__':
    main()
