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
    scene.transition("off")


def check(bri, setpoint):
    return abs(bri - setpoint) < 0.01


away_values = [
        [27, 0.173],
        [32, 0.133],
        [46, 0.055],
    ]


def main():
    for lamp, value in away_values:
        if not check(_phue.get_bri(lamp), value):
            break
        sleep(.1)
    else:
        print("away")
        away()
        exit()


if __name__ == "__main__":
    main()
