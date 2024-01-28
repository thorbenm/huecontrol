#!/usr/bin/python3
import _phue
from time import sleep
import sys
sys.path.insert(0, '/home/pi/Programming/roomba')
import roomba
import ambient
import scene
from datetime import datetime


def home():
    if ambient.should_be_off():
        scene.transition("off_wohnzimmer")
    else:
        scene.transition("scheduled_wohnzimmer")
    scene.transition("scheduled_schlafzimmer")
    sleep(1.0)
    if 12 <= datetime.now().hour <= 16:  # TODO: no time should be here.
        ambient.auto_ct_fast_reduce_only()
    roomba.stop()


def away():
    scene.transition("off")
    roomba.start()


def check(bri, setpoint):
    return abs(bri - setpoint) < 0.01


home_values = [
        ["Ananas", 0.03937007874015748],
        ["Fensterlampe", 0.11811023622047244],
        ["Hue Go", 0.1889763779527559],
        ["LED Streifen", 0.11023622047244094],
        ["Stehlampe", 0.20866141732283464]
    ]


away_values = [
        ["Ananas", 0.16141732283464566],
        ["Fensterlampe", 0.03937007874015748],
        ["Hue Go", 0.051181102362204724],
        ["LED Streifen", 0.2283464566929134],
        ["Stehlampe", 0.031496062992125984]
    ]


for lamp, value in home_values:
    if not check(_phue.get_bri(lamp), value):
        break
    sleep(.1)
else:
    home()
    exit()


for lamp, value in away_values:
    if not check(_phue.get_bri(lamp), value):
        break
    sleep(.1)
else:
    away()
