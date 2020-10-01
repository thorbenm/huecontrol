#!/usr/bin/python3
import requests
from time import sleep
from time import time
import json
import _phue
from math import inf
from user_id import user_id

json_data = requests.get("https://discovery.meethue.com").json()
ip_address = json_data[0]['internalipaddress']

class Sensor():
    def __init__(self, sensor_id, lights, turn_off_after):
        self.sensor_id = sensor_id
        self.lights = lights
        self.turn_off_after = turn_off_after
        self.current_state = None
        self.last_motion = inf
        self.master = 'Stehlampe'
        self.master_state = None
        self.minimum = 0.01
        self.maximum = 1.0

    def get_sensor_state(self):
        response = requests.get("http://%s/api/%s/sensors/%d" % (
                                ip_address, user_id, self.sensor_id))
        json_data = json.loads(response.text)
        return json_data['state']['presence']

    def slave(self, slaves):
        bri = _phue.get_bri(self.master)
        bri = max(min(bri, self.maximum), self.minimum)
        ct = _phue.get_ct(self.master)
        
        _phue.set_lights(slaves, bri=bri, ct=ct)
        self.master_state = bri

    def turn_lights(self, state):
        if state != self.current_state:
            self.current_state = state
            if state:
                self.slave(self.lights)
            else:
                _phue.set_lights(self.lights, on=False, time=10.0)

    def update(self):
        state = self.get_sensor_state()
        if _phue.get_bri(self.master) != self.master_state:
            self.current_state = None
        if state:
            self.last_motion = time()
            self.turn_lights(True)
        if self.last_motion + self.turn_off_after < time():
            self.turn_lights(False)


kuchen_sensor = Sensor(10, ["Deckenleuchte Links", "Deckenleuchte Rechts"], 180.0)


while True:
    kuchen_sensor.update()
    sleep(0.1)
