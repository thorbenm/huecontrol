#!/usr/bin/python3
import requests
from phue import Bridge


json_data = requests.get("https://discovery.meethue.com").json()
ip_address = json_data[0]['internalipaddress']


b = Bridge(ip_address)
b.connect()


def set_lights(lights, bri=None, ct=None, on=None, hue=None, sat=None, time=.4):
    time = int(time * 10)

    for l in lights:
        if on is not None:
            b.set_light(l, 'on', on, transitiontime=time)
        if bri is not None:
            current_state = b.get_light(l, 'on')
            # if the light is currently off it will not react to
            # new brightness settings, so we have to turn it
            # on first
            if current_state is False and 1.0 / 254.0 < bri:
                b.set_light(l, 'on', True, transitiontime=time)
            if 1.0 / 254.0 < bri:
                b.set_light(l, 'bri', int(bri * 254), transitiontime=time)
            else:
                b.set_light(l, 'on', False, transitiontime=time)
        if ct is not None:
            b.set_light(l, 'ct', int(ct * (454 - 153) + 153), transitiontime=time)
        if hue is not None:
            b.set_light(l, 'hue', int(hue * 65535), transitiontime=time)
        if sat is not None:
            b.set_light(l, 'sat', int(sat * 254), transitiontime=time)


def get_bri(light):
    if not b.get_light(light, "on"):
        return 0.0
    return float(b.get_light(light, "bri")) / 254.0


def get_ct(light):
    return (float(b.get_light(light, "ct")) - 153.0) / (454.0 - 153.0)
