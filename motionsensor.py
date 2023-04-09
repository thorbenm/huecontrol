#!/usr/bin/python3
import requests
from time import sleep
from time import time
import json
import _phue
from math import inf
from math import isclose
from personal_data import user_id
import os.path
import os
from pathlib import Path
import ambient
from datetime import datetime
from systemd import journal


def freeze():
    Path("/home/pi/Programming/huecontrol/motionsensor_freeze").touch()


def _map(x, in_min, in_max, out_min, out_max):
    # arduino map
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


class Sensor():
    master = "Stehlampe"
    master_bri = float('nan')
    master_ct = float('nan')
    ambient_bri = float('nan')
    next_update = -inf
    def __init__(self, sensor_id, lights, turn_off_after, mock_file=None,
                 use_ambient=False):
        self.sensor_id = sensor_id
        self.lights = lights
        self.turn_off_after = turn_off_after
        self.last_motion = time() if _phue.is_on(lights[0]) else -inf
        self.mock_file = mock_file

        self.current_bri = float('nan')
        self.current_ct = float('nan')

        self.minimum_bri = _phue.min_bri()
        self.maximum_bri = 1.0

        self.minimum_ct = 0.3
        self.maximum_ct = 1.0

        self.use_ambient = use_ambient

        self.last_sensor_state_buffer = None

    def get_master_bri(self):
        try:
            bri = _phue.get_bri(Sensor.master)
            bri = _map(bri, 0.0, 1.0, self.minimum_bri, self.maximum_bri)
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
            Sensor.next_update = time() + 90.0
            os.remove("motionsensor_freeze")

    def get_virtual_ct(self, bri, minimum_ct=None):
        # based on brightness instead
        if minimum_ct is None:
            minimum_ct = self.minimum_ct
        if bri < 0.5:
            return self.maximum_ct
        else:
            return _map(bri, 0.5, 1.0, self.maximum_ct, minimum_ct)

    def get_master_ct(self):
        try:
            if not _phue.is_on(Sensor.master):
                return 1.0

            ct = _phue.get_ct(Sensor.master)
            ct = _map(ct, 0.0, 1.0, self.minimum_ct, self.maximum_ct)
            return max(ct, self.get_virtual_ct(Sensor.master_bri))
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

    def update_shared_values(self):
        if Sensor.next_update < time():
            Sensor.master_bri = self.get_master_bri()
            Sensor.master_ct = self.get_master_ct()
            Sensor.ambient_bri = ambient.get_simulated_brightness()
            Sensor.next_update = time() + 5.0

    def get_bri_ct(self):
        master_bri = Sensor.master_bri
        master_ct = Sensor.master_ct
        ambient_bri = Sensor.ambient_bri
        ambient_ct = self.get_virtual_ct(Sensor.ambient_bri, minimum_ct=.65)
        if master_bri < ambient_bri and self.use_ambient:
            return ambient_bri, ambient_ct
        else:
            return master_bri, master_ct

    def update(self):
        self.freeze_file()
        self.update_shared_values()
        if self.sensor_state() or self.mock_file_exists():
            self.last_motion = time()

        bri, ct = self.get_bri_ct()

        master_changed = (not isclose(bri, self.current_bri) or
                          not isclose(ct, self.current_ct))
        if self.sensor_state_buffer_changed():
            if self.sensor_state_buffer():
                journal.write("bri=%.2f, ct=%.2f " % (bri, ct) +
                              " ".join(self.lights))
                _phue.set_lights_safe(self.lights, bri=bri, ct=ct)
                self.current_bri = bri
                self.current_ct = ct
            else:
                _phue.set_lights(self.lights, on=False, time=10.0)
        elif master_changed:
            if self.sensor_state_buffer():
                t = 0.4
                if (abs(bri - self.current_bri) < 0.09 and
                        abs(ct - self.current_ct) < 0.09):
                    t = 4.5

                journal.write("bri=%.2f, ct=%.2f " % (bri, ct) +
                              " ".join(self.lights))
                _phue.set_lights(self.lights, bri=bri, ct=ct, time=t)
                self.current_bri = bri
                self.current_ct = ct


def main():
    kuchen_sensor = Sensor(10, ["Deckenleuchte Links", "Deckenleuchte Rechts", "Filament"],
                           300.0, mock_file="mock_kuche")
    flur_sensor = Sensor(33, ["Kronleuchter"], 120.0, use_ambient=True)
    bad_sensor = Sensor(81, ["Badlicht", "Spiegellicht"], 600.0, use_ambient=True)


    while True:
        kuchen_sensor.update()
        sleep(.05)
        flur_sensor.update()
        sleep(.05)
        bad_sensor.update()
        sleep(.05)
        _phue.check_lights()
        sleep(.05)


if __name__ == '__main__':
    main()
