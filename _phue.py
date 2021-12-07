#!/usr/bin/python3
import requests
from phue import Bridge
from time import sleep


ip_address = "Philips-hue"
b = Bridge(ip_address)
b.connect()


def set_lights(lights, bri=None, ct=None, on=None, hue=None, sat=None, time=.4,
               reduce_only=False):
    if type(lights) == str:
        lights = [lights]

    time = int(time * 10)

    for l in lights:
        if on is not None:
            if reduce_only and not is_on(l):
                continue
            set_light(l, 'on', on, transitiontime=time)
        if ct is not None:
            set_light(l, 'ct', int(ct * (454 - 153) + 153), transitiontime=time)
        if hue is not None:
            set_light(l, 'hue', int(hue * 65535), transitiontime=time)
        if sat is not None:
            set_light(l, 'sat', int(sat * 254), transitiontime=time)
        if bri is not None:
            if reduce_only and get_bri(l) < bri:
                continue
            current_state = b.get_light(l, 'on')
            # if the light is currently off it will not react to
            # new brightness settings, so we have to turn it
            # on first
            if current_state is False and 1.0 / 254.0 < bri:
                set_light(l, 'on', True, transitiontime=time)
#            if 1.0 / 254.0 < bri:
            set_light(l, 'bri', int(bri * 254), transitiontime=time)
#            else:
#                set_light(l, 'on', False, transitiontime=time)


def is_on(light):
    return b.get_light(light, "on")


def get_bri(light):
    if not b.get_light(light, "on"):
        return 0.0
    return float(b.get_light(light, "bri")) / 254.0


def get_ct(light):
    return (float(b.get_light(light, "ct")) - 153.0) / (454.0 - 153.0)


set_light=b.set_light


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
