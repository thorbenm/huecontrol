#!/usr/bin/python3
import sys
from time import sleep
from _phue import set_lights
from _phue import is_on
from _phue import get_bri
import argparse
import motionsensor


def hell(time=.4, reduce_only=False):
    if 90 < time:
        motionsensor.freeze()
    set_lights(["Hue Go", "Stehlampe", "Fensterlampe", "LED Streifen"],
               bri=1.0, ct=0.0, time=time, reduce_only=reduce_only)
    set_lights(["Hängelampe"], bri=1.0, time=time, reduce_only=reduce_only)
    set_lights(["Lichterkette"], on=True, time=time, reduce_only=reduce_only)


def hell_schlafzimmer(time=.4, reduce_only=False):
    set_lights(["Tischlampe"], bri=1.0, ct=0.0, time=time, reduce_only=reduce_only)
    set_lights(["Schlafzimmer Hängelampe"], bri=1.0, time=time, reduce_only=reduce_only)


def warm(time=.4, reduce_only=False):
    if 90 < time:
        motionsensor.freeze()
    set_lights(["Hue Go", "Stehlampe", "Fensterlampe", "LED Streifen"],
               bri=1.0, ct=0.4, time=time, reduce_only=reduce_only)
    set_lights(["Hängelampe"], bri=1.0, time=time, reduce_only=reduce_only)
    set_lights(["Lichterkette"], on=True, time=time, reduce_only=reduce_only)


def warm_schlafzimmer(time=.4, reduce_only=False):
    set_lights(["Tischlampe"], bri=1.0, ct=0.4, time=time, reduce_only=reduce_only)
    set_lights(["Schlafzimmer Hängelampe"], bri=1.0, time=time, reduce_only=reduce_only)


def lesen(time=.4, reduce_only=False):
    if 90 < time:
        motionsensor.freeze()
    set_lights(["Hue Go", "Stehlampe", "Fensterlampe", "LED Streifen"], bri=1.0, ct=1.0, time=time, reduce_only=reduce_only)
    set_lights(["Hängelampe"], on=True, bri=.3, time=time, reduce_only=reduce_only)
    set_lights(["Lichterkette"], on=True, time=time, reduce_only=reduce_only)


def lesen_schlafzimmer(time=.4, reduce_only=False):
    set_lights(["Tischlampe"], bri=1.0, ct=1.0, time=time, reduce_only=reduce_only)
    set_lights(["Schlafzimmer Hängelampe"], on=True, bri=.3, time=time, reduce_only=reduce_only)


def gemutlich(time=.4, reduce_only=False, bri=.5):
    if 90 < time:
        motionsensor.freeze()
    set_lights(["Hue Go", "Stehlampe", "Fensterlampe", "LED Streifen"], bri=bri, ct=1.0, time=time, reduce_only=reduce_only)
    set_lights(["Hängelampe"], on=False, time=time, reduce_only=reduce_only)
    set_lights(["Lichterkette"], on=True, time=time, reduce_only=reduce_only)


def gemutlich_schlafzimmer(time=.4, reduce_only=False, bri=.5):
    set_lights(["Tischlampe"], bri=bri, ct=1.0, time=time, reduce_only=reduce_only)
    set_lights(["Schlafzimmer Hängelampe"], on=False, time=time, reduce_only=reduce_only)


def dunkel(time=.4, reduce_only=False):
    if 90 < time:
        motionsensor.freeze()
    set_lights(["Hue Go", "Stehlampe", "Fensterlampe", "LED Streifen"], bri=.1, ct=1.0, time=time, reduce_only=reduce_only)
    set_lights(["Hängelampe"], on=False, time=time, reduce_only=reduce_only)
    set_lights(["Lichterkette"], on=True, time=time, reduce_only=reduce_only)


def dunkel_schlafzimmer(time=.4, reduce_only=False):
    set_lights(["Tischlampe"], bri=.1, ct=1.0, time=time, reduce_only=reduce_only)
    set_lights(["Schlafzimmer Hängelampe"], on=False, time=time, reduce_only=reduce_only)


def off(time=.4, reduce_only=False):
    if 90 < time:
        motionsensor.freeze()
    set_lights(["Hue Go", "Stehlampe", "Fensterlampe", "Hängelampe",
                "Lichterkette", "LED Streifen"],
               on=False, time=time, reduce_only=reduce_only)


def off_schlafzimmer(time=.4, reduce_only=False):
    set_lights(["Tischlampe", "Schlafzimmer Hängelampe"],
               on=False, time=time, reduce_only=reduce_only)


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
