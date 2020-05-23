#!/usr/bin/python3
import sys
from _phue import set_lights


try:
    t = float(sys.argv[2])
except:
    t = .4


t *= 60 # minutes
t *= 10 # hue api uses 1/10 of a second as unit
t = int(t)


def hell():
   set_lights(["Hue Go", "Stehlampe", "Fensterlampe"], bri=255, ct=0, time=t)
   set_lights(["Hängelampe"], on=True, time=t)
   set_lights(["Hängelampe"] ,bri=255, time=t)
   set_lights(["Lichterkette"], on=True, time=t)


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
