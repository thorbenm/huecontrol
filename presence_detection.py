#!/usr/bin/python3
import _phue
from time import sleep
import sys
sys.path.insert(0, '/home/pi/Programming/roomba')
import roomba
import ambient
import scene
import scheduled_scene


def home():
    # scheduled_scene.transition_schlafzimmer()
    if ambient.should_be_off():
        scene.transition(name="off", room="wohnzimmer")
    else:
        scheduled_scene.transition(room="wohnzimmer")
    sleep(1.0)
    if ambient.auto_ct_enabled():
        ambient.auto_ct_fast_reduce_only()
    # roomba.stop()


def away():
    scene.transition("off")
    # roomba.start()


def check(bri, setpoint):
    return abs(bri - setpoint) < 0.01


home_values = [
        ["Stehlampe", 0.212],
        ["Sofalampe Links", 0.063],
        ["Sofalampe Rechts", 0.185],
    ]


away_values = [
        ["Stehlampe", 0.035],
        ["Sofalampe Links", 0.193],
        ["Sofalampe Rechts", 0.114],
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
