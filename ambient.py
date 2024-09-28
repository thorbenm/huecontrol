#!/usr/bin/python3

from hue_data import user_id
from datetime import datetime
import requests
import json
import _phue
import logging
from numpy import mean, log
import scene
import data
from time import sleep, time
import toolbox
import sys
import schedule


log_file = '/home/pi/ambient.log'
MASTER = 89


def trim_logs():
    with open(log_file, "r") as file:
        lines = file.readlines()

    max_number_of_lines = 1 * 24 * 60

    if len(lines) > max_number_of_lines:
        with open(log_file, "w") as file:
            file.writelines(lines[-max_number_of_lines:])


def __get_new(i=MASTER):
    response = requests.get("http://%s/api/%s/sensors/%d" % (
                            _phue.ip_address, user_id, i))
    json_data = json.loads(response.text)
    return json_data["state"]["lightlevel"]


def __get_history(i=MASTER, number=10):
    with open(log_file, "r") as file:
        lines = file.readlines()
    if len(lines) == 0:
        sleep(.1)
        with open(log_file, "r") as file:
            lines = file.readlines()

    if number != float('inf'):
        lines = lines[-number:]
    lines_copy = lines
    try:
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
    except:
        print(lines_copy)
        raise


def get_history_mean(i=MASTER, number=10):
    return mean(__get_history(i, number))


def get_simulated_bri():
    # snowy nights in winter can be up to 3500 in brightness,
    # so 4000 makes sure simulated brightness is 0 all night
    # the hightest values I have seen are around 40000. So
    # 36000 is just slighty lower than that.

    g = get_history_mean()
    bri = toolbox.map(g, 4000, 29000, 0, 1, clamp=True)
    curvature_from = .6
    curvature_to = .6
    bri = bri ** (log(curvature_to)/log(curvature_from))
    return bri


def get_schmitt_trigger(low=16000, high=20000):
    history = __get_history(number=float('inf'))
    for j in history[::-1]:
        if j <= low:
            return False
        elif high <= j:
            return True
 

def log_all():
    message = ""
    for i in [MASTER, 11, 31, 34, 82]:
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
    trim_logs()


def __minutes_in_current_day():
    now = datetime.now()
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    minutes_passed = (now - midnight).total_seconds() // 60
    return int(minutes_passed)


limit_ambient = 35000.0
limit_minutes = int(1 * 60)
def should_turn_off():
    window_minutes = __minutes_in_current_day()
    if window_minutes < limit_minutes:
        return False
    history = __get_history(number=window_minutes)
    history_before = history[:-1]
    nof_elements = len([h for h in history if limit_ambient <= h])
    nof_elements_before = len([h for h in history_before if limit_ambient <= h])
    return (nof_elements == limit_minutes and
            nof_elements_before == limit_minutes - 1)


def should_be_off():
    window_minutes = __minutes_in_current_day()
    if window_minutes < limit_minutes:
        return False
    history = __get_history(number=window_minutes)
    nof_elements = len([h for h in history if limit_ambient <= h])
    return limit_minutes <= nof_elements


def turn_off_if_ambient_above_limit():
    if should_turn_off():
        scene.transition('off_wohnzimmer')


def auto_ct_slow_reduce_only(transition_time=14*60):
    if transition_time is None:
        transition_time = AUTO_CT_TRANSITION_TIME - 1.0
    bri = get_simulated_bri()
    s = toolbox.scene_superposition(bri, data.hell,
                                    1.0 - bri, data.halbwarm)
    scene.transition_dicionary(s, time=transition_time, reduce_only=True)


def auto_ct_fast_reduce_only(transition_time=.4):
    auto_ct_slow_reduce_only(transition_time=transition_time)


def auto_ct_enabled():
    return schedule.get_variable("auto_ct")


def main():
    log_all()
    turn_off_if_ambient_above_limit()
    trim_logs()
    minute = datetime.now().minute
    if auto_ct_enabled() and minute % 15 == 0:
        auto_ct_slow_reduce_only()


if __name__ == "__main__":
    if len(sys.argv) == 1:
        main()
    else:
        for a in sys.argv[1:]:
            f = globals()[a.strip("-").replace("-", "_")]
            f()
