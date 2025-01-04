#!/usr/bin/python3
import _phue
import data


def main():
    lights = data.get_lights("kinderzimmer")
    _phue.set_lights(lights[1:], on=False)
    _phue.set_lights(lights[0], ct=1.0, time=30)
    _phue.set_lights(lights[0], on=False, time=3*60)


if __name__ == '__main__':
    main()
