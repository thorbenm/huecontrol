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


def is_on(light):
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


global_d = dict()


def set_lights_save(lights, **kwargs):
    global global_d
    set_lights(lights, **kwargs)
    if "time" in kwargs:
        if .5 < kwargs["time"]:
            return
    if "bri" in kwargs:
        if kwargs["bri"] < 0.09:
            return
    d = dict()
    for l in [lights] if type(lights) == str else lights:
        d[l] = {**kwargs, "at": time() + 90.0}
    global_d = {**global_d, **d}


def values_ok(set_v, get_v):
    if isinstance(set_v, bool) and isinstance(get_v, bool):
        return set_v == get_v
    if isinstance(set_v, float) and isinstance(get_v, float):
        return 0.09 < get_v


def check_lights():
    global global_d
    for l in list(global_d.keys()):
        if global_d[l]["at"] < time():
            dd = {j:global_d[l][j] for j in global_d[l] if j != "at"}
            for k in list(dd.keys()):
                set_v = dd[k]
                if k == "on":
                    get_v = is_on(l)
                else:
                    get_v = eval("get_" + k + "(\"" + l + "\")")
                if values_ok(set_v, get_v):
                    del dd[k]
            if dd:
                set_lights(l, **dd)
            del global_d[l]


def min_bri():
    return 1.1/254.0
