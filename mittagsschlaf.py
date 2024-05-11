#!/usr/bin/python3
import _phue
import data


def main():
    lights = data.schlafzimmer_lights
    lights = [l[0] for l in lights]
    lights = [l for l in lights if l != "Wickeltischlampe"]
    _phue.set_lights(lights, on=False)
    _phue.set_lights("Wickeltischlampe", ct=1.0, time=60)
    _phue.set_lights("Wickeltischlampe", bri=_phue.min_bri(), time=5*60)


if __name__ == '__main__':
    main()
