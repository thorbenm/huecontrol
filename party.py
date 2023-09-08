#!/usr/bin/python3
import _phue
import random
from time import sleep

lamps = ["Hue Go", "Fensterlampe", "LED Streifen", "Ananas"]
settings = [[0.559, 0.960], [0.846, 0.640], [0.649, 0.759], [0.303, 0.472], [0.319, 0.0]]

counter = 0

def _sleep(time):
    global counter
    for _ in range(int(time)):
        if _phue.get_bri("Stehlampe") < 0.05:
            counter += 1
        else:
            counter = 0
        if 5 < counter:
            exit()
        sleep(1.0)


def main():
    while True:
        r1 = float(random.randint(20, 60))
        r2 = float(random.randint(20, 60))
        lamp = random.choice(lamps)
        setting = random.choice(settings)
        sat = setting[0]
        hue = setting[1]
        _phue.set_lights(lamp, sat=sat, hue=hue, bri=.75, time=r1)
        _sleep(r1 + r2)


if __name__ == '__main__':
    main()
