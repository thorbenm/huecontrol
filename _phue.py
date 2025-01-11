#!/usr/bin/python3
import requests
from phue import Bridge
from time import time as unix_time
from hue_data import ip_address
import json
import toolbox
import os


b = Bridge(ip_address)
b.connect()


def set_lights(lights, bri=None, ct=None, on=None, hue=None, sat=None, time=.4,
               reduce_only=False, increase_only=False):

    command = {'transitiontime' : int(time * 10)}
    if on is not None:
        command["on"] = on
    if bri is not None:
        command["bri"] = int(bri * 254)
    if ct is not None:
        command["ct"] = int(ct * (454 - 153) + 153)
    if hue is not None:
        command["hue"] = int(hue * 65535)
    if sat is not None:
        command["sat"] = int(hue * 254)
    if "on" not in command.keys():
        if "bri" in command.keys():
            command["on"] = 0 < command["bri"]
        else:
            command["on"] = True

    if not reduce_only and not increase_only:
        set_fake_values(lights, time=time, bri=bri, ct=ct)
        set_light(lights, command)
    elif reduce_only:
        for l in [lights] if type(lights) == str else lights:
            command_c = command.copy()
            command_c["on"] = min(command_c["on"], b.get_light(l, "on"))
            if "bri" in command_c.keys():
                current_bri = b.get_light(l, "bri") if b.get_light(l, "on") else 0
                if current_bri < command_c["bri"]:
                    command_c.pop("bri")
            if "ct" in command_c.keys():
                current_ct = b.get_light(l, "ct") if b.get_light(l, "on") else 454
                if command_c["ct"] < current_ct:
                    command_c.pop("ct")

            set_fake_values(l, time=time,
                            bri=(bri if "bri" in command_c else None),
                            ct=(ct if "ct" in command_c else None))
            set_light(l, command_c)
    elif increase_only:
        for l in [lights] if type(lights) == str else lights:
            command_c = command.copy()
            command_c["on"] = max(command_c["on"], b.get_light(l, "on"))
            if "bri" in command_c.keys():
                current_bri = b.get_light(l, "bri") if b.get_light(l, "on") else 0
                if command_c["bri"] < current_bri:
                    command_c.pop("bri")
            if "ct" in command_c.keys():
                current_ct = b.get_light(l, "ct") if b.get_light(l, "on") else 454
                if current_ct < command_c["ct"]:
                    command_c.pop("ct")

            set_fake_values(l, time=time,
                            bri=(bri if "bri" in command_c else None),
                            ct=(ct if "ct" in command_c else None))
            set_light(l, command_c)


def get_on(light):
    return b.get_light(light, "on")


def __get_bri(light):
    return float(b.get_light(light, "bri")) / 254.0


def get_bri(light):
    if b.get_light(light, "on"):
        ret = __get_bri(light)
    else:
        # homekit only sets "on" and leaves "bri" at its original
        # value when using the hue switch to turn off a light
        ret = 0.0
    fake = get_fake_value(light, "bri", ret)
    if fake is None:
        return ret
    else:
        return fake


def convert_mirek_to_ct(mirek):
    return toolbox.map(mirek, 153, 454, 0, 1)


def __get_ct(light):
    return convert_mirek_to_ct(b.get_light(light, "ct"))


def get_ct(light):
    ret = float("NaN")
    if not b.get_light(light, "on"):
        ret = 1.0
    try:
        # try catch is a workaround for lazy implementation of light that
        # dont support ct in motionsensor
        ret = __get_ct(light)
    except:
        ret = 1.0
    fake = get_fake_value(light, "ct", ret)
    if fake is None:
        return ret
    else:
        return fake


def set_light(*args, **kwargs):
    # print(*args, **kwargs)
    b.set_light(*args, **kwargs)


def get_hue(light):
    return float(b.get_light(light, "hue")) / 65535


def get_sat(light):
    return float(b.get_light(light, "sat")) / 254


global_l = list()


def set_lights_safe(lights, **kwargs):
    # global global_d
    global global_l
    set_lights(lights, **kwargs)
    if "time" in kwargs:
        if .5 < kwargs["time"]:
            return
    if "bri" in kwargs:
        if kwargs["bri"] < 0.09:
            return
    else:
        return
    if type(lights) == str:
        return
    if len(lights) == 1:
        return
    global_l.append({"at": unix_time() + 90.0,
                     "lights": lights,
                     "bri": kwargs["bri"]})


def check_lights():
    global global_l
    for elem in global_l[:]:
        if elem["at"] < unix_time():
            l0 = elem["lights"][0]
            b0 = get_bri(l0)
            for l in elem["lights"][1:]:
                b = get_bri(l)
                if 0.02 < abs(b0 - b):
                    set_lights(elem["lights"], bri=elem["bri"])
                    break
            global_l.remove(elem)


def min_bri():
    return 1.1/254.0


FAKE_VALUES_PATH = "/home/pi/fake_values.json"
FAKE_LAMPS = ["Stehlampe"]
FAKE_DURATION = 120.0


def set_fake_values(lights, time, bri=None, ct=None):
    if 1.0 < time:
        d = dict()
        for l in [lights] if type(lights) == str else lights:
            if l not in FAKE_LAMPS:
                continue
            d[l] = dict()
            if bri is not None:
                start_bri = __get_bri(l)
                finish_bri = bri
                if 0.02 < abs(start_bri - finish_bri):
                    d[l]["start_bri"] = start_bri
                    d[l]["finish_bri"] = finish_bri
            if ct is not None:
                start_ct = __get_ct(l)
                finish_ct = ct
                if 0.02 < abs(start_ct - finish_ct):
                    d[l]["start_ct"] = start_ct
                    d[l]["finish_ct"] = finish_ct
            if d[l]:
                d[l]["start_time"] = unix_time()
                d[l]["finish_time"] = d[l]["start_time"] + time
            else:
                del d[l]
        if d:
            with open(FAKE_VALUES_PATH, 'w') as f:
                json.dump(d, f)


def get_fake_value(light, kind, real_value):
    if light in FAKE_LAMPS:
        d = dict()
        try:
            with open(FAKE_VALUES_PATH, 'r') as f:
                d = json.load(f)
        except FileNotFoundError:
            return None
        if light in d:
            if unix_time() - d[light]["start_time"] < FAKE_DURATION:
                if "start_" + kind in d[light] and "finish_" + kind in d[light]:
                    start = d[light]["start_" + kind]
                    finish = d[light]["finish_" + kind]
                    if abs(real_value - finish) < .02 or abs(real_value - start) < .02:
                        return toolbox.map(unix_time(),
                                           d[light]["start_time"],
                                           d[light]["finish_time"],
                                           start, finish, clamp=True)
                    else:
                        os.remove(FAKE_VALUES_PATH)
            else:
                os.remove(FAKE_VALUES_PATH)
    # to support multiple FAKE_LAMPS remove should delete the entry of this one and
    # not delete the entire file
    return None
