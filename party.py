#!/usr/bin/python3
import _phue
from random import choice
from time import sleep


lamps = ["Hue Go", "Fensterlampe", "LED Streifen", "Ananas"]
settings = [[0.559, 0.960], [0.846, 0.640], [0.649, 0.759], [0.303, 0.472], [0.319, 0.0]]


def main():
    start_bri = _phue.get_bri("Stehlampe")
    while abs(_phue.get_bri("Stehlampe") - start_bri) < .02:
        lamp = choice(lamps)
        setting = choice(settings)
        sat, hue = setting
        _phue.set_lights(lamp, sat=sat, hue=hue, time=120)
        sleep(120)


if __name__ == '__main__':
    main()
