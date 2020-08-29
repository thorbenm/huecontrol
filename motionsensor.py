#!/usr/bin/python3
import requests
from time import sleep
from time import time
import json
import _phue
from math import inf

json_data = requests.get("https://discovery.meethue.com").json()
ip_address = json_data[0]['internalipaddress']

user_id = "8V16CtsH4x-IPzPsI1AUMzMAP4eL8PJeWPoJjmXu"

class Sensor():
    def __init__(self, sensor_id, lights, turn_off_after):
        self.sensor_id = sensor_id
        self.lights = lights
        self.turn_off_after = turn_off_after
        self.current_state = None
        self.last_motion = inf

    def get_sensor_state(self):
        response = requests.get("http://%s/api/%s/sensors/%d" % (
                                ip_address, user_id, self.sensor_id))
        json_data = json.loads(response.text)
        return json_data['state']['presence']

    def slave(self, slaves):
        master = 'Stehlampe'
        minimum = 0.1
        maximum = 1.0
        
        bri = _phue.get_bri(master)
        bri = max(min(bri, maximum), minimum)
        ct = _phue.get_ct(master)
        
        _phue.set_lights(slaves, bri=bri, ct=ct)

    def turn_lights(self, state):
        if state != self.current_state:
            self.current_state = state
            if state:
                self.slave(self.lights)
            else:
                _phue.set_lights(self.lights, on=False, time=20.0)

    def update(self):
        state = self.get_sensor_state()
        if state:
            self.last_motion = time()
            self.turn_lights(True)
        if self.last_motion + self.turn_off_after < time():
            self.turn_lights(False)


dielen_sensor = Sensor(33, ["Dielenlicht"], 60.0)


while True:
    dielen_sensor.update()

#last_motion = inf
#turn_off_after = 30.0
#while True:
#    state = get_sensor_state(33)
#    if state:
#        last_motion = time()
#        turn_light(True)
#    if last_motion + turn_off_after < time():
#        turn_light(False)
#   
#    sleep(0.1)
