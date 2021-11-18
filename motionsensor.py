#!/usr/bin/python3
import requests
from time import sleep
from time import time
import json
import _phue
from math import inf
from math import isclose
from user_id import user_id
import os.path
import os
from pathlib import Path


def freeze():
    Path("/home/pi/Programming/huecontrol/motionsensor_freeze").touch()


class Sensor():
    master = "Stehlampe"
    master_bri = float('nan')
    master_ct = float('nan')
    next_update = -inf
    def __init__(self, sensor_id, lights, turn_off_after, mock_file=None):
        self.sensor_id = sensor_id
        self.lights = lights
        self.turn_off_after = turn_off_after
        self.last_motion = inf if _phue.is_on(lights[0]) else -inf
        self.mock_file = mock_file

        self.current_bri = float('nan')
        self.current_ct = float('nan')

        self.minimum_bri = _phue.min_bri()
        self.maximum_bri = 1.0

        self.last_sensor_state_buffer = None

    def get_master_bri(self):
        try:
            bri = _phue.get_bri(Sensor.master)
            bri = max(min(bri, self.maximum_bri), self.minimum_bri)
            return bri
        except:
            return 0.5

    def mock_file_exists(self):
        if self.mock_file is not None:
            if os.path.isfile(self.mock_file):
                return True
        return False

    def freeze_file(self):
        if os.path.isfile("motionsensor_freeze"):
            Sensor.next_update = time() + 40.0
            os.remove("motionsensor_freeze")

    def get_master_ct(self):
        try:
            def _map(x, in_min, in_max, out_min, out_max):
                # arduino map
                return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
            if not _phue.is_on(Sensor.master):
                return 1.0

            ct = _phue.get_ct(Sensor.master)
            if 0.98 < ct:
                return 1.0
            if Sensor.master_bri < 0.5:
                return 1.0
            else:
                return _map(Sensor.master_bri, 0.5, 1.0, 1.0, 0.5)
        except:
            return 1.0

    def sensor_state(self):
        try:
            response = requests.get("http://%s/api/%s/sensors/%d" % (
                                    _phue.ip_address, user_id, self.sensor_id))
            json_data = json.loads(response.text)
            return json_data['state']['presence']
        except:
            # requests very rarely throws an exception.
            # mostly during the night that causes the whole thing to crash
            # todo: catch the specific exception
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

    def update_bri_ct(self):
        if Sensor.next_update < time():
            master_bri = Sensor.master_bri
            master_ct = Sensor.master_ct
            Sensor.master_bri = self.get_master_bri()
            Sensor.master_ct = self.get_master_ct()
            master_bri_changed = not isclose(master_bri, Sensor.master_bri)
            master_ct_changed = not isclose(master_ct, Sensor.master_ct)
            Sensor.next_update = time() + 5.0
            return master_bri_changed or master_ct_changed
        return False


    def update(self):
        self.freeze_file()
        self.update_bri_ct()
        if self.sensor_state() or self.mock_file_exists():
            self.last_motion = time()
        master_changed = (not isclose(Sensor.master_bri, self.current_bri) or
                          not isclose(Sensor.master_ct, self.current_ct))
        if self.sensor_state_buffer_changed():
            if self.sensor_state_buffer():
                # print("bri=%.2f, ct=%.2f" % (Sensor.master_bri, Sensor.master_ct))
                _phue.set_lights(self.lights, bri=Sensor.master_bri,
                                 ct=Sensor.master_ct)
                self.current_bri = Sensor.master_bri
                self.current_ct = Sensor.master_ct
            else:
                _phue.set_lights(self.lights, on=False, time=10.0)
            return
        if master_changed:
            if self.sensor_state_buffer():
                t = 0.4
                if (abs(Sensor.master_bri - self.current_bri) < 0.2 and
                        abs(Sensor.master_ct - self.current_ct) < 0.2):
                    t = 5.0
                # print("bri=%.2f, ct=%.2f" % (Sensor.master_bri, Sensor.master_ct))
                _phue.set_lights(self.lights, bri=Sensor.master_bri,
                                 ct=Sensor.master_ct, time=t)
                self.current_bri = Sensor.master_bri
                self.current_ct = Sensor.master_ct


def main():
    kuchen_sensor = Sensor(10, ["Deckenleuchte Links", "Deckenleuchte Rechts", "Filament"], 300.0, mock_file="mock_kuche")
    flur_sensor = Sensor(33, ["Kronleuchter"], 120.0)
    bad_sensor = Sensor(81, ["Badlicht", "Spiegellicht"], 600.0)


    while True:
        kuchen_sensor.update()
        sleep(.05)
        flur_sensor.update()
        sleep(.05)
        bad_sensor.update()
        sleep(.05)


if __name__ == '__main__':
    main()
