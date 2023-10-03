#!/usr/bin/python3
import requests
from phue import Bridge
from time import sleep, time
from personal_data import ip_address


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

        set_light(lights, command)
    elif reduce_only:
        for l in [lights] if type(lights) == str else lights:
            command_c = command.copy()
            command_c["on"] = min(command_c["on"], b.get_light(l, "on"))
            if "bri" in command_c.keys():
                current_bri = b.get_light(l, "bri") if b.get_light(l, "on") else 0
                if current_bri < command_c["bri"]:
                    # print("pop bri=%d" % command_c["bri"])
                    command_c.pop("bri")
            if "ct" in command_c.keys():
                current_ct = b.get_light(l, "ct") if b.get_light(l, "on") else 454
                if command_c["ct"] < current_ct:
                    # print("pop ct=%d" % command_c["ct"])
                    command_c.pop("ct")

            set_light(l, command_c)
    elif increase_only:
        for l in [lights] if type(lights) == str else lights:
            command_c = command.copy()
            command_c["on"] = max(command_c["on"], b.get_light(l, "on"))
            if "bri" in command_c.keys():
                current_bri = b.get_light(l, "bri") if b.get_light(l, "on") else 0
                if command_c["bri"] < current_bri:
                    # print("pop bri=%d" % command_c["bri"])
                    command_c.pop("bri")
            if "ct" in command_c.keys():
                current_ct = b.get_light(l, "ct") if b.get_light(l, "on") else 454
                if current_ct < command_c["ct"]:
                    # print("pop ct=%d" % command_c["ct"])
                    command_c.pop("ct")

            set_light(l, command_c)


def get_on(light):
    return b.get_light(light, "on")


def get_bri(light):
    if not b.get_light(light, "on"):
        return 0.0
    return float(b.get_light(light, "bri")) / 254.0


def get_ct(light):
    if not b.get_light(light, "on"):
        return 1.0
    try:
        # try catch is a workaround for lazy implementation of light that
        # dont support ct in motionsensor
        return (float(b.get_light(light, "ct")) - 153.0) / (454.0 - 153.0)
    except:
        return 1.0


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
    global_l.append({"at": time() + 90.0,
                     "lights": lights,
                     "bri": kwargs["bri"]})


def check_lights():
    global global_l
    for elem in global_l[:]:
        if elem["at"] < time():
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
