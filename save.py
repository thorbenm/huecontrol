import _phue
import data
import json
import os


FILE_PATH = "/home/pi/saved_lights.json"


def save():
    dictionary = dict()
    for light, light_data in data.all_lights:
        dictionary[light] = dict()
        for d in light_data:
            dictionary[light][d] = eval("_phue.get_%s('%s')" % (
                                        d, light))
    with open(FILE_PATH, "w") as f:
        json.dump(dictionary, f)


def saved_data_exists():
    return os.path.isfile(FILE_PATH)


def apply(delete=True):
    if not saved_data_exists():
        return {}

    with open(FILE_PATH, "r") as f:
        dictionary = json.load(f)

    if delete:
       os.remove(FILE_PATH)

    for light, light_data in dictionary.items():
        _phue.set_lights(light, **light_data)
