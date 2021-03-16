#!/usr/bin/python3
import sys
from time import sleep
from _phue import set_lights
from _phue import is_on
from _phue import get_bri
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-s', type=str, required=True, dest='scene')
parser.add_argument('-t', type=str, default='0.4s', dest='time')
parser.add_argument('--reduce-only', action='store_true', dest='reduce_only')
args = parser.parse_args()


unit_is_minutes = False
if args.time.endswith("m"):
    unit_is_minutes = True
time = float(args.time[:-1])
if unit_is_minutes:
    time *= 60


def hell(time):
    set_lights(["Hue Go", "Stehlampe", "Fensterlampe", "LED Streifen"], bri=1.0, ct=0.0, time=time, reduce_only=args.reduce_only)
    set_lights(["Hängelampe"], bri=1.0, time=time, reduce_only=args.reduce_only)
    set_lights(["Lichterkette"], on=True, time=time, reduce_only=args.reduce_only)


def hell_schlafzimmer(time):
    set_lights(["Tischlampe"], bri=1.0, ct=0.0, time=time, reduce_only=args.reduce_only)
    set_lights(["Schlafzimmer Hängelampe"], bri=1.0, time=time, reduce_only=args.reduce_only)


def wakeup(time):
    assert not args.reduce_only, "wakeup should not be called with --reduce-only"

    ignore_schlafzimmer = False
    ignore_wohnzimmer = 0.9 < get_bri("Stehlampe")

    if not ignore_schlafzimmer:
        set_lights(["Tischlampe"], bri=2.0/254.0, ct=1.0, time=.4)
    if not ignore_wohnzimmer:
        set_lights(["Hue Go", "Stehlampe", "Fensterlampe", "LED Streifen"], bri=2.0/254.0, ct=1.0, time=.4)

    sleep(1.0)

    if not ignore_schlafzimmer:
        gemutlich_schlafzimmer(time)
    if not ignore_wohnzimmer:
        gemutlich(time / 2.0)

    sleep(time + 1.0)

    if not ignore_schlafzimmer and is_on("Tischlampe"):
        hell_schlafzimmer(600.0)
    if not ignore_wohnzimmer and is_on("Stehlampe"):
        hell(600.0)


def lesen(time):
    set_lights(["Hue Go", "Stehlampe", "Fensterlampe", "LED Streifen"], bri=1.0, ct=1.0, time=time, reduce_only=args.reduce_only)
    set_lights(["Hängelampe"], on=True, time=time, reduce_only=args.reduce_only)
    set_lights(["Hängelampe"], bri=1.0, time=time, reduce_only=args.reduce_only)
    set_lights(["Lichterkette"], on=True, time=time, reduce_only=args.reduce_only)


def warm(time):
    set_lights(["Hue Go", "Stehlampe", "Fensterlampe", "LED Streifen"], ct=1.0, time=time)


def warm_schlafzimmer(time):
    set_lights(["Tischlampe"], ct=1.0, time=time)


def lesen_schlafzimmer(time):
    set_lights(["Tischlampe"], bri=1.0, ct=1.0, time=time, reduce_only=args.reduce_only)
    set_lights(["Schlafzimmer Hängelampe"], on=False, time=time, reduce_only=args.reduce_only)


def gemutlich(time):
    set_lights(["Hue Go", "Stehlampe", "Fensterlampe", "LED Streifen"], bri=.5, ct=1.0, time=time, reduce_only=args.reduce_only)
    set_lights(["Hängelampe"], on=False, time=time, reduce_only=args.reduce_only)
    set_lights(["Lichterkette"], on=True, time=time, reduce_only=args.reduce_only)


def gemutlich_schlafzimmer(time):
    set_lights(["Tischlampe"], bri=.5, ct=1.0, time=time, reduce_only=args.reduce_only)
    set_lights(["Schlafzimmer Hängelampe"], on=False, time=time, reduce_only=args.reduce_only)


def dunkel(time):
    set_lights(["Hue Go", "Stehlampe", "Fensterlampe", "LED Streifen"], bri=.1, ct=1.0, time=time, reduce_only=args.reduce_only)
    set_lights(["Hängelampe"], on=False, time=time, reduce_only=args.reduce_only)
    set_lights(["Lichterkette"], on=True, time=time, reduce_only=args.reduce_only)


def dunkel_schlafzimmer(time):
    set_lights(["Tischlampe"], bri=.1, ct=1.0, time=time, reduce_only=args.reduce_only)
    set_lights(["Schlafzimmer Hängelampe"], on=False, time=time, reduce_only=args.reduce_only)


def off(time):
    set_lights(["Hue Go", "Stehlampe", "Fensterlampe", "Hängelampe",
                "Lichterkette", "Tischlampe", "Schlafzimmer Hängelampe",
                "LED Streifen"],
               on=False, time=time, reduce_only=args.reduce_only)


exec("%s(%f)" % (args.scene, time))
