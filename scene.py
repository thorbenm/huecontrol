#!/usr/bin/python3
from _phue import set_lights
import argparse
import motionsensor
import data


def find_duplicate_values(dictionary):
    values_to_keys = {}
    result_keys = []
    result_values = []

    for key, value in dictionary.items():
        value_str = str(value)
        if value_str in values_to_keys:
            index = values_to_keys[value_str]
            result_keys[index].append(key)
        else:
            values_to_keys[value_str] = len(result_keys)
            result_keys.append([key])
            result_values.append(value)

    return result_keys, result_values


def transition(name, time=.4, reduce_only=False, increase_only=False,
              _override={}):
    if name.endswith("zimmer"):
        if 90.0 < time and name.endswith("wohnzimmer"):
            motionsensor.freeze()
        d = eval("data." + name)
        d = {**d, **_override}
        keys, values = find_duplicate_values(d)
        for k, v in zip(keys, values):
            set_lights(k, **v, time=time, reduce_only=reduce_only,
                       increase_only=increase_only)
    else:
        transition(name + "_wohnzimmer", time=time, reduce_only=reduce_only,
                  increase_only=increase_only, _override=_override)
        transition(name + "_schlafzimmer", time=time, reduce_only=reduce_only,
                  increase_only=increase_only, _override=_override)


def convert_time_string(time_str):
    unit_is_minutes = False
    if time_str.endswith("m"):
        unit_is_minutes = True
    time = float(time_str[:-1].replace(",", "."))
    if unit_is_minutes:
        time *= 60
    return time


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', type=str, required=True, dest='scene')
    parser.add_argument('-t', type=str, default='0.4s', dest='time')
    parser.add_argument('--reduce-only', action='store_true', dest='reduce_only')
    parser.add_argument('-c', action='store_true', dest='scheduled')
    args = parser.parse_args()

    time = convert_time_string(args.time)

    if args.scene.startswith("scheduled"):
        with open("/home/pi/scheduled_scene", "r") as f:
            scheduled = f.read().replace("\n", "")
            args.scene = args.scene.replace("scheduled", scheduled)

    transition(args.scene, time=time, reduce_only=args.reduce_only)
    if args.scheduled:
        with open("/home/pi/scheduled_scene", "w") as file:
            file.write(args.scene.split("_")[0] + "\n")



if __name__ == '__main__':
    main()
