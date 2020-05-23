#!/usr/bin/python3
import sys
from _phue import set_lights

try:
    t_str = sys.argv[2]
    if t_str.endswith("s"):
        unit_is_minutes = False
    elif t_str.endswith("m"):
        unit_is_minutes = True
    t_str = t_str[:-1]
    t = float(t_str)
except:
    t = .4


if unit_is_minutes:
    t *= 60
t *= 10 # hue api uses 1/10th of a second as unit
t = int(t)


def hell():
    set_lights(["Hue Go", "Stehlampe", "Fensterlampe"], bri=255, ct=0, time=t)
    set_lights(["Hängelampe"], on=True, time=t)
    set_lights(["Hängelampe"] ,bri=255, time=t)
    set_lights(["Lichterkette"], on=True, time=t)

def wakeup():
    hell()
    set_lights(["Tischlampe"], bri=255, ct=0, time=t)

def lesen():
    set_lights(["Hue Go", "Stehlampe", "Fensterlampe"], bri=255, ct=500, time=t)
    set_lights(["Hängelampe"], on=True, time=t)
    set_lights(["Hängelampe"] ,bri=255, time=t)
    set_lights(["Lichterkette"], on=True, time=t)


def gemutlich():
    set_lights(["Hue Go", "Stehlampe", "Fensterlampe"], bri=153, ct=500, time=t)
    set_lights(["Hängelampe"], on=False, time=t)
    set_lights(["Lichterkette"], on=True, time=t)


exec(sys.argv[1] + "()")
