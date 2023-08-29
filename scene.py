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
    set_lights(["Lichterkette"], on=(min_bri() <= bri), time=time, reduce_only=reduce_only, increase_only=increase_only)


def __schlafzimmer_prototype(bri, bri_h, ct, time, reduce_only, increase_only):
    set_lights(["Nachttischlampe"], bri=bri, ct=ct, time=time, reduce_only=reduce_only, increase_only=increase_only)
    set_lights(["Wickeltischlampe"], bri=bri, ct=ct, time=time, reduce_only=reduce_only, increase_only=increase_only)
    set_lights(["Schlafzimmer Hängelampe"], bri=bri_h, time=time, reduce_only=reduce_only, increase_only=increase_only)


def focus(*args, **kwargs):
    focus_wohnzimmer(*args, **kwargs)
    focus_schlafzimmer(*args, **kwargs)


def focus_wohnzimmer(time=.4, reduce_only=False, increase_only=False):
    __wohnzimmer_prototype(bri=1.0, bri_h=1.0, ct=0, time=time, reduce_only=reduce_only, increase_only=increase_only)


def focus_schlafzimmer(time=.4, reduce_only=False, increase_only=False):
    __schlafzimmer_prototype(bri=1.0, bri_h=1.0, ct=0, time=time, reduce_only=reduce_only, increase_only=increase_only)


def hell(*args, **kwargs):
    hell_wohnzimmer(*args, **kwargs)
    hell_schlafzimmer(*args, **kwargs)


def hell_wohnzimmer(time=.4, reduce_only=False, increase_only=False):
    __wohnzimmer_prototype(bri=1.0, bri_h=1.0, ct=.35, time=time, reduce_only=reduce_only, increase_only=increase_only)


def hell_schlafzimmer(time=.4, reduce_only=False, increase_only=False):
    __schlafzimmer_prototype(bri=1.0, bri_h=1.0, ct=.35, time=time, reduce_only=reduce_only, increase_only=increase_only)


def halbwarm(*args, **kwargs):
    halbwarm_wohnzimmer(*args, **kwargs)
    halbwarm_schlafzimmer(*args, **kwargs)


def halbwarm_wohnzimmer(time=.4, reduce_only=False, increase_only=False):
    __wohnzimmer_prototype(bri=1.0, bri_h=1.0, ct=.6, time=time, reduce_only=reduce_only, increase_only=increase_only)


def halbwarm_schlafzimmer(time=.4, reduce_only=False, increase_only=False):
    __schlafzimmer_prototype(bri=1.0, bri_h=1.0, ct=.6, time=time, reduce_only=reduce_only, increase_only=increase_only)


def max(*args, **kwargs):
    max_wohnzimmer(*args, **kwargs)
    max_schlafzimmer(*args, **kwargs)


def max_wohnzimmer(time=.4, reduce_only=False, increase_only=False):
    __wohnzimmer_prototype(bri=1.0, bri_h=.3, ct=1.0, time=time, reduce_only=reduce_only, increase_only=increase_only)


def max_schlafzimmer(time=.4, reduce_only=False, increase_only=False):
    __schlafzimmer_prototype(bri=1.0, bri_h=.3, ct=1.0, time=time, reduce_only=reduce_only, increase_only=increase_only)


def warm(*args, **kwargs):
    warm_wohnzimmer(*args, **kwargs)
    warm_schlafzimmer(*args, **kwargs)


def warm_wohnzimmer(time=.4, reduce_only=False, increase_only=False):
    __wohnzimmer_prototype(bri=.75, bri_h=0, ct=1.0, time=time, reduce_only=reduce_only, increase_only=increase_only)


def warm_schlafzimmer(time=.4, reduce_only=False, increase_only=False):
    __schlafzimmer_prototype(bri=.75, bri_h=0, ct=1.0, time=time, reduce_only=reduce_only, increase_only=increase_only)


def gemutlich(*args, **kwargs):
    gemutlich_wohnzimmer(*args, **kwargs)
    gemutlich_schlafzimmer(*args, **kwargs)


def gemutlich_wohnzimmer(time=.4, reduce_only=False, increase_only=False):
    __wohnzimmer_prototype(bri=.4, bri_h=0, ct=1.0, time=time, reduce_only=reduce_only, increase_only=increase_only)


def gemutlich_schlafzimmer(time=.4, reduce_only=False, increase_only=False):
    __schlafzimmer_prototype(bri=.4, bri_h=0, ct=1.0, time=time, reduce_only=reduce_only, increase_only=increase_only)


def dunkel(*args, **kwargs):
    dunkel_wohnzimmer(*args, **kwargs)
    dunkel_schlafzimmer(*args, **kwargs)


def dunkel_wohnzimmer(time=.4, reduce_only=False, increase_only=False):
    __wohnzimmer_prototype(bri=.1, bri_h=0, ct=1.0, time=time, reduce_only=reduce_only, increase_only=increase_only)


def dunkel_schlafzimmer(time=.4, reduce_only=False, increase_only=False):
    __schlafzimmer_prototype(bri=.1, bri_h=0, ct=1.0, time=time, reduce_only=reduce_only, increase_only=increase_only)


def lesen(*args, **kwargs):
    lesen_wohnzimmer(*args, **kwargs)
    lesen_schlafzimmer(*args, **kwargs)


def lesen_wohnzimmer(time=.4, reduce_only=False, increase_only=False):
    if 90 < time:
        motionsensor.freeze()
    set_lights(["Hue Go", "Stehlampe", "LED Streifen", "Ananas"],
               bri=.1, ct=1.0, time=time, reduce_only=reduce_only, increase_only=increase_only)
    set_lights(["Fensterlampe"],
               bri=.4, ct=1.0, time=time, reduce_only=reduce_only, increase_only=increase_only)
    set_lights(["Hängelampe"], bri=0.0, time=time, reduce_only=reduce_only, increase_only=increase_only)
    set_lights(["Lichterkette"], on=False, time=time, reduce_only=reduce_only, increase_only=increase_only)


def lesen_schlafzimmer(time=.4, reduce_only=False, increase_only=False):
    set_lights(["Nachttischlampe"], bri=.3, ct=1.0, time=time, reduce_only=reduce_only, increase_only=increase_only)
    set_lights(["Wickeltischlampe"], bri=min_bri(), ct=1.0, time=time, reduce_only=reduce_only, increase_only=increase_only)
    set_lights(["Schlafzimmer Hängelampe"], on=False, reduce_only=reduce_only, increase_only=increase_only)


def min(*args, **kwargs):
    min_wohnzimmer(*args, **kwargs)
    min_schlafzimmer(*args, **kwargs)


def min_wohnzimmer(time=.4, reduce_only=False, increase_only=False):
    __wohnzimmer_prototype(bri=min_bri(), bri_h=0, ct=1.0, time=time, reduce_only=reduce_only, increase_only=increase_only)


def min_schlafzimmer(time=.4, reduce_only=False, increase_only=False):
    __schlafzimmer_prototype(bri=min_bri(), bri_h=0, ct=1.0, time=time, reduce_only=reduce_only, increase_only=increase_only)


def nachtlicht_schlafzimmer(time=.4, reduce_only=False, increase_only=False):
    set_lights(["Nachttischlampe"], on=False, time=time, reduce_only=reduce_only, increase_only=increase_only)
    set_lights(["Wickeltischlampe"], bri=min_bri(), ct=1.0, time=time, reduce_only=reduce_only, increase_only=increase_only)
    set_lights(["Schlafzimmer Hängelampe"], on=False, reduce_only=reduce_only, increase_only=increase_only)


def off(*args, **kwargs):
    off_wohnzimmer(*args, **kwargs)
    off_schlafzimmer(*args, **kwargs)


def off_wohnzimmer(time=.4, reduce_only=False, increase_only=False):
    __wohnzimmer_prototype(bri=0, bri_h=0, ct=1.0, time=time, reduce_only=reduce_only, increase_only=increase_only)


def off_schlafzimmer(time=.4, reduce_only=False, increase_only=False):
    __schlafzimmer_prototype(bri=0, bri_h=0, ct=1.0, time=time, reduce_only=reduce_only, increase_only=increase_only)


def convert_time_string(time_str):
    unit_is_minutes = False
    if time_str.endswith("m"):
        unit_is_minutes = True
    time = float(time_str[:-1].replace(",", "."))
    if unit_is_minutes:
        time *= 60
    return time


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', type=str, required=True, dest='scene')
    parser.add_argument('-t', type=str, default='0.4s', dest='time')
    parser.add_argument('--reduce-only', action='store_true', dest='reduce_only')
    parser.add_argument('-c', action='store_true', dest='scheduled')
    args = parser.parse_args()

    time = convert_time_string(args.time)

    if args.scene.startswith("scheduled"):
        with open("/home/pi/scheduled_scene", "r") as f:
            scheduled = f.read().replace("\n", "")
            args.scene = args.scene.replace("scheduled", scheduled)

    exec("%s(%f, reduce_only=%s)" % (args.scene, time, "True" if args.reduce_only else "False"))
    if args.scheduled:
        with open("/home/pi/scheduled_scene", "w") as file:
            file.write(args.scene.split("_")[0] + "\n")



if __name__ == '__main__':
    main()
