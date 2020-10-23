#!/usr/bin/python3
import requests
from time import sleep
from time import time
import json
import _phue
from math import inf
from user_id import user_id
import os.path

json_data = requests.get("https://discovery.meethue.com").json()
ip_address = json_data[0]['internalipaddress']

class Sensor():
    def __init__(self, sensor_id, lights, turn_off_after, mock_file=None, master="Stehlampe"):
        self.sensor_id = sensor_id
        self.lights = lights
        self.turn_off_after = turn_off_after
        self.last_motion = inf if _phue.is_on(lights[0]) else -inf
        self.master = master
        self.master_bri = None
        self.master_ct = None
        self.mock_file = mock_file

        self.minimum_bri = 1.1/255.0
        self.maximum_bri = 1.0

        self.minimum_ct = 0.5
        self.maximum_ct = 1.0

        self.last_sensor_state_buffer = None

    def get_master_bri(self):
        bri = _phue.get_bri(self.master)
        bri = max(min(bri, self.maximum_bri), self.minimum_bri)
        return bri

    def mock_file_exists(self):
        if self.mock_file is not None:
            print("testing")
            if os.path.isfile(self.mock_file):
                print ("File exist")
                return True
            print ("File not exist")
        return False

    def get_master_ct(self):
        if not _phue.is_on(self.master):
            return 1.0
        try:
            ct = _phue.get_ct(self.master)
            ct = max(min(ct, self.maximum_ct), self.minimum_ct)
            return ct
        except:
            return 1.0

    def sensor_state(self):
        response = requests.get("http://%s/api/%s/sensors/%d" % (
                                ip_address, user_id, self.sensor_id))
        json_data = json.loads(response.text)
        return json_data['state']['presence']

    def master_bri_changed(self):
        new_bri = self.get_master_bri()
        if (self.master_bri != new_bri):
            self.master_bri = new_bri
            return True
        return False

    def master_ct_changed(self):
        new_ct = self.get_master_ct()
        if (self.master_ct != new_ct):
            self.master_ct = new_ct
            return True
        return False

    def sensor_state_buffer(self):
        if self.last_motion + self.turn_off_after < time():
            return False
        return True

    def sensor_state_buffer_changed(self):
        new_state = self.sensor_state_buffer()
        if self.last_sensor_state_buffer != new_state:
            self.last_sensor_state_buffer = new_state
            return True
        return False

    def slave(self):
        bri = self.get_master_bri()
        ct = self.get_master_ct()
        
        _phue.set_lights(self.lights, bri=bri, ct=ct)

    def update(self):
        if self.sensor_state() or self.mock_file_exists():
            self.last_motion = time()
        if (self.sensor_state_buffer_changed() or
                self.master_bri_changed() or self.master_ct_changed()):
            if self.sensor_state_buffer():
                self.slave()
            else:
                _phue.set_lights(self.lights, on=False, time=10.0)


kuchen_sensor = Sensor(10, ["Deckenleuchte Links", "Deckenleuchte Rechts", "Filament"], 300.0, mock_file="mock_kuche")
flur_sensor = Sensor(33, ["Kronleuchter"], 120.0)
bad_sensor = Sensor(81, ["Badlicht", "Spiegellicht"], 600.0)


while True:
    try:
        kuchen_sensor.update()
        sleep(.05)
        flur_sensor.update()
        sleep(.05)
        bad_sensor.update()
        sleep(.05)
    except:
        pass
