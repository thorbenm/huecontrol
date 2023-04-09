#!/usr/bin/python3

from personal_data import user_id
import requests
import json
import _phue
import logging
from numpy import mean
import scene


log_file = '/home/pi/ambient.log'
MASTER = 11


def arduino_map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def trim_logs():
    with open(log_file, "r") as file:
        lines = file.readlines()

    if len(lines) > 10000:
        with open(log_file, "w") as file:
            file.writelines(lines[-10000:])


def __get_new(i=MASTER):
    response = requests.get("http://%s/api/%s/sensors/%d" % (
                            _phue.ip_address, user_id, i))
    json_data = json.loads(response.text)
    return json_data["state"]["lightlevel"]


def __get_history(i=MASTER, number=10):
    with open(log_file, "r") as file:
        lines = file.readlines()
    lines = lines[-number:]
    lines = [l.replace("\n", "") for l in lines]
    lines = [l[26:] for l in lines]
    lines = [l.split(";") for l in lines]
    lines = [[jj.replace(" ", "") for jj in j if jj] for j in lines]
    lines = [[jj for jj in j if jj] for j in lines]
    data = dict()
    for l in lines:
        for element in l:
            key, value = element.split(':')
            key = int(key)
            value = float(value)
            if key not in data:
                data[key] = list()
            data[key].append(value)
    return data[i]


def get_history_mean(i=MASTER, number=10):
    return mean(__get_history(i, number))


def get_simulated_brightness():
    m = get_history_mean()
    bri = arduino_map(m, 5000, 25000, 0, 1)
    bri = min(bri, 1)
    bri = max(bri, 0)
    return bri
 

def log_all():
    message = ""
    for i in [11, 31, 34, 82]:
        lightlevel = __get_new(i)
    
        message += str(i) 
        message += ": "
        message += str(lightlevel)
        message += "; "
    
    logging.basicConfig(filename=log_file,
                        encoding='utf-8',
                        level=logging.INFO,
                        format='%(asctime)s   %(message)s')
    logging.info(message)


limit = 30000.0
window_minutes = int(60)
def should_turn_off():
    h = __get_history(number=window_minutes)
    history = h[:-1]
    now = h[-1]
    return max(history) < limit and limit <= now


def should_be_off():
    history = __get_history(number=window_minutes)
    return limit <= max(history)


def turn_off_if_ambient_above_limit():
    if should_turn_off():
        scene.off_wohnzimmer(time=10*60)


def main():
    log_all()
    turn_off_if_ambient_above_limit()
    trim_logs()


if __name__ == "__main__":
    main()
