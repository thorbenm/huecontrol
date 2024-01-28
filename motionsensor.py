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
import ambient
from systemd import journal
import scene
import data
import toolbox


class Sensor():
    master = "Stehlampe"
    master_bri = float('nan')
    master_ct = float('nan')
    ambient_bri = float('nan')
    currently_using_ambient_brightness = None
    scheduled_ct = float('nan')
    next_update = -inf
    def __init__(self, sensor_id, lights, turn_off_after, mock_file=None,
                 use_ambient_for_brightness=False, use_ambient_for_motion=False):
        self.sensor_id = sensor_id
        self.lights = lights
        self.turn_off_after = turn_off_after
        self.last_motion = time() if _phue.get_on(lights[0]) else -inf
        self.mock_file = mock_file

        self.current_bri = float('nan')
        self.current_ct = float('nan')

        self.minimum_bri = _phue.min_bri()
        self.maximum_bri = 1.0

        self.minimum_ct = 0.3
        self.maximum_ct = 1.0

        self.use_ambient_for_brightness = use_ambient_for_brightness
        self.use_ambient_for_motion = use_ambient_for_motion

        self.last_sensor_state_buffer = None

    def get_master_bri(self):
        try:
            return _phue.get_bri(Sensor.master)
        except:
            return 0.5

    def apply_min_max_bri(self, bri):
        minimum_bri = self.minimum_bri
        if self.use_ambient_for_motion and ambient.get_schmitt_trigger():
            minimum_bri = 0.0
        return toolbox.map(bri, 0.0, 1.0, minimum_bri, self.maximum_bri)

    def mock_file_exists(self):
        if self.mock_file is not None:
            if os.path.isfile(self.mock_file):
                return True
        return False

    def get_virtual_ct(self, bri, minimum_ct=None):
        # based on brightness instead
        if minimum_ct is None:
            minimum_ct = self.minimum_ct
        if bri < 0.5:
            return self.maximum_ct
        else:
            return toolbox.map(bri, 0.5, 1.0, self.maximum_ct, minimum_ct)

    def get_master_ct(self):
        try:
            if not _phue.get_on(Sensor.master):
                return 1.0

            ct = _phue.get_ct(Sensor.master)
            ct = toolbox.map(ct, 0.0, 1.0, self.minimum_ct, self.maximum_ct)
            return ct
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

    def get_scheduled_ct(self):
        scheduled_scene = scene.get_scheduled_scene()
        d = eval("data." + scheduled_scene)
        ct = d[Sensor.master]["ct"]
        ct = toolbox.map(ct, 1.0, 0.0, self.maximum_ct, self.minimum_ct)
        return ct

    def update_shared_values(self):
        if Sensor.next_update < time():
            Sensor.master_bri = self.get_master_bri()
            Sensor.master_ct = self.get_master_ct()
            Sensor.ambient_bri = ambient.get_simulated_bri()
            Sensor.currently_using_ambient_brightness = Sensor.master_bri < Sensor.ambient_bri
            Sensor.scheduled_ct = self.get_scheduled_ct()
            Sensor.next_update = time() + 5.0

    def get_bri_ct(self):
        master_bri = Sensor.master_bri
        master_ct = Sensor.master_ct
        ambient_bri = Sensor.ambient_bri
        if 0.01 < master_bri:
            ambient_ct = master_ct
        else:
            ambient_ct = Sensor.scheduled_ct
        if Sensor.currently_using_ambient_brightness and self.use_ambient_for_brightness:
            return ambient_bri, ambient_ct
        else:
            return master_bri, master_ct

    def update(self):
        self.update_shared_values()
        if self.sensor_state() or self.mock_file_exists():
            self.last_motion = time()

        bri, ct = self.get_bri_ct()
        bri = self.apply_min_max_bri(bri)

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
                if abs(bri - self.current_bri) < 0.25:
                    t = 4.9

                journal.write("bri=%.2f, ct=%.2f " % (bri, ct) +
                              " ".join(self.lights))
                _phue.set_lights(self.lights, bri=bri, ct=ct, time=t)
                self.current_bri = bri
                self.current_ct = ct


def main():
    kuchen_sensor = Sensor(10, ["Deckenleuchte Links", "Deckenleuchte Rechts", "Filament"],
                           300.0, mock_file="mock_kuche", use_ambient_for_motion=True)
    flur_sensor = Sensor(33, ["Kronleuchter"], 120.0, use_ambient_for_brightness=True)
    bad_sensor = Sensor(81, ["Badlicht", "Spiegellicht"], 600.0, use_ambient_for_brightness=True)


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
