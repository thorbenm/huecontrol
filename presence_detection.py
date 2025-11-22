#!/usr/bin/python3
import _phue
from time import sleep
import sys
sys.path.insert(0, '/home/pi/Programming/roomba')
import roomba
import ambient
import scene
import scheduled_scene


def away():
    scene.transition("off", rooms=["wohnzimmer", "kinderzimmer", "arbeitszimmer"])


def home():
    scheduled_scene.transition(rooms=["wohnzimmer"])
    roomba.stop()


def check(bri, setpoint):
    return abs(bri - setpoint) < 0.01


away_values = [
        [27, 0.173],
        [32, 0.133],
        [46, 0.055],
    ]

home_values = [
        [27, 0.055],
        [32, 0.224],
        [46, 0.094],
    ]


def main():
    if all(check(_phue.get_bri(lamp), value) for lamp, value in away_values):
        print("away")
        away()
    elif all(check(_phue.get_bri(lamp), value) for lamp, value in home_values):
        print("home")
        home()


if __name__ == "__main__":
    main()
