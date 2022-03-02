#!/usr/bin/python3
import requests
from phue import Bridge
from time import sleep
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
    return (float(b.get_light(light, "ct")) - 153.0) / (454.0 - 153.0)


def set_light(*args, **kwargs):
    # print(*args, **kwargs)
    b.set_light(*args, **kwargs)


def set_light_save(*args, **kwargs):
    # currently unused. The problem wasnt that the light setting function
    # didnt throw an error but that it pretends everything was fine when
    # the light in fact was never controlled.
    # not sure if i should try and work with the monitor value instead.
    # for now ill just not use it at all.
    for _ in range(3):
        r = []
        try:
            r = b.set_light(*args, **kwargs)
            # print(r)
            assert len(r) == 1
            r = r[0]
            assert len(r) == 2
            try:
                if list(r[1].values())[0]['description'] == 'parameter, ct, not available':
                    r = r[:-1]
            except:
                pass
            for j in r:
                k = list(j.keys())
                assert len(k) == 1
                assert k[0] == 'success'
            return
        except:
            print(r)
        sleep(2.0)


def min_bri():
    return 1.1/254.0
