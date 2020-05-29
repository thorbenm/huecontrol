#!/usr/bin/python3
import sys
from time import sleep
from _phue import set_lights
from _phue import is_on


if len(sys.argv) == 2:
    t_str = "0.4s"
else:
    t_str = sys.argv[2]


unit_is_minutes = False
if t_str.endswith("m"):
    unit_is_minutes = True
t_str = t_str[:-1]
t = float(t_str)
if unit_is_minutes:
    t *= 60
t_str = str(t)


def hell(time):
    set_lights(["Hue Go", "Stehlampe", "Fensterlampe"], bri=1.0, ct=0.0, time=time)
    set_lights(["Hängelampe"], bri=1.0, time=time)
    set_lights(["Lichterkette"], on=True, time=time)


def wakeup(time):
    set_lights(["Tischlampe", "Hue Go", "Stehlampe", "Fensterlampe"], bri=2.0/254.0, ct=1.0, time=.4)
    sleep(1.0)
    lesen(time / 2.0)
    set_lights(["Tischlampe"], bri=1.0, ct=1.0, time=time / 2.0)
    sleep(time / 2.0 + 1.0)
    if is_on("Stehlampe"):
        hell(time / 2.0)
    if is_on("Tischlampe"):
        set_lights(["Tischlampe"], bri=1.0, ct=0.0, time=time / 2.0)


def lesen(time):
    set_lights(["Hue Go", "Stehlampe", "Fensterlampe"], bri=1.0, ct=1.0, time=time)
    set_lights(["Hängelampe"], on=True, time=time)
    set_lights(["Hängelampe"], bri=1.0, time=time)
    set_lights(["Lichterkette"], on=True, time=time)


def gemutlich(time):
    set_lights(["Hue Go", "Stehlampe", "Fensterlampe"], bri=.6, ct=1.0, time=time)
    set_lights(["Hängelampe"], on=False, time=time)
    set_lights(["Lichterkette"], on=True, time=time)


def dunkel(time):
    set_lights(["Hue Go", "Stehlampe", "Fensterlampe"], bri=.1, ct=1.0, time=time)
    set_lights(["Hängelampe"], on=False, time=time)
    set_lights(["Lichterkette"], on=True, time=time)


def off(time):
    set_lights(["Hue Go", "Stehlampe", "Fensterlampe", "Hängelampe",
                "Lichterkette", "Tischlampe", "Schlafzimmer Hängelampe"],
               on=False, time=time)


exec(sys.argv[1].lower() + "(" + t_str + ")")
