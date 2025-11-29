#!/usr/bin/python3
import asyncio
from aiohue.v2 import HueBridgeV2
from hue_data import ip_address, user_id  # Import IP and API key
from aiohue.v2.models.resource import ResourceTypes
import _phue
import light_ids
import os
import ambient
import data
import toolbox
import scheduled_scene
from math import isnan
import subprocess
import scene
import scheduled_scene
import systemd.journal
import time
import sys
import datetime
import traceback


MASTER_NAME = {r: data.get_lights(r)[0] for r in data.get_rooms()}
MASTER_ID = {r: light_ids.get_id(n) for r, n in MASTER_NAME.items()}
AMBIENT_SENSOR_ID = "9dd345e1-d99a-40eb-8cfd-25209e90ebfd"
BALCONY_MOTION_SENSOR = "dd4438ac-d357-4378-9b31-d4d92dd4911f"


all_sensors = list()


global_brightness_values = {k: _phue.get_bri(k) for k in data.get_lights("all", include_slaves=True) if k != "Lichterkette"}
global_on_values = {k: _phue.get_on(k) for k in data.get_lights("all", include_slaves=True) if k != "Lichterkette"}
global_ambient_value = ambient.get_simulated_bri()


def running_under_systemd():
    return os.environ.get('INVOCATION_ID') is not None


def log(*args, **kwargs):
    message = " ".join(str(arg) for arg in args)
    systemd.journal.write(message)
    if not running_under_systemd():
        print(message, **kwargs)


log(f"ambient brightness: {global_ambient_value:.3g}")


class Switch():
    def __init__(self, ):
        self.long_press_duration = 1
        if not isinstance(self.long_press_duration, int):
            raise RuntimeError("long_press_duration must be an integer")
        self.repeat_counter = 0

        self.on_short_press_function = None
        self.up_short_press_function = None
        self.down_short_press_function = None
        self.off_short_press_function = None

        self.on_long_press_function = None
        self.up_long_press_function = None
        self.down_long_press_function = None
        self.off_long_press_function = None

        self.on_hold_function = None
        self.up_hold_function = None
        self.down_hold_function = None
        self.off_hold_function = None

        self.on_double_press_function = None
        self.up_double_press_function = None
        self.down_double_press_function = None
        self.off_double_press_function = None

        self.on_tripple_press_function = None
        self.up_tripple_press_function = None
        self.down_tripple_press_function = None
        self.off_tripple_press_function = None

        self.on_quadruple_press_function = None
        self.up_quadruple_press_function = None
        self.down_quadruple_press_function = None
        self.off_quadruple_press_function = None

        self.multi_press_time_threshold = 5.0

        self.button_history = list()
        self.button_history_max_length = 10

    def add_to_button_history(self, button):
        self.button_history.append({"button": button, "timestamp": time.time()})
        self.button_history = self.button_history[-self.button_history_max_length:]

    def get_button_matches(self, button):
        return len([b for b in self.button_history if b["button"] == button and time.time() - self.multi_press_time_threshold < b["timestamp"]])

    def is_double_press(self, button):
        return self.get_button_matches(button) == 2

    def is_tripple_press(self, button):
        return self.get_button_matches(button) == 3

    def is_quadruple_press(self, button):
        return self.get_button_matches(button) == 4

    def set_on_short_press_function(self, f):
        self.on_short_press_function = f

    def set_on_double_press_function(self, f):
        self.on_double_press_function = f

    def set_on_tripple_press_function(self, f):
        self.on_tripple_press_function = f

    def set_on_quadruple_press_function(self, f):
        self.on_quadruple_press_function = f

    def set_up_short_press_function(self, f):
        self.up_short_press_function = f

    def set_down_short_press_function(self, f):
        self.down_short_press_function = f

    def set_off_short_press_function(self, f):
        self.off_short_press_function = f

    def set_off_double_press_function(self, f):
        self.off_double_press_function = f

    def set_off_tripple_press_function(self, f):
        self.off_tripple_press_function = f

    def set_off_quadruple_press_function(self, f):
        self.off_quadruple_press_function = f

    def set_on_long_press_function(self, f):
        if self.on_hold_function is not None:
            raise RuntimeError("on_long_press_function and on_hold_function cannot both be set")
        self.on_long_press_function = f

    def set_up_long_press_function(self, f):
        if self.up_hold_function is not None:
            raise RuntimeError("up_long_press_function and up_hold_function cannot both be set")
        self.up_long_press_function = f

    def set_down_long_press_function(self, f):
        if self.down_hold_function is not None:
            raise RuntimeError("down_long_press_function and down_hold_function cannot both be set")
        self.down_long_press_function = f

    def set_off_long_press_function(self, f):
        if self.off_hold_function is not None:
            raise RuntimeError("off_long_press_function and off_hold_function cannot both be set")
        self.off_long_press_function = f

    def set_on_hold_function(self, f):
        if self.on_long_press_function is not None:
            raise RuntimeError("on_long_press_function and on_hold_function cannot both be set")
        self.on_hold_function = f

    def set_up_hold_function(self, f):
        if self.up_long_press_function is not None:
            raise RuntimeError("up_long_press_function and up_hold_function cannot both be set")
        self.up_hold_function = f

    def set_down_hold_function(self, f):
        if self.down_long_press_function is not None:
            raise RuntimeError("down_long_press_function and down_hold_function cannot both be set")
        self.down_hold_function = f

    def set_off_hold_function(self, f):
        if self.off_long_press_function is not None:
            raise RuntimeError("off_long_press_function and off_hold_function cannot both be set")
        self.off_hold_function = f

    def button_event(self, button, event):
        if event != "repeat":
            self.repeat_counter = 0

        if event == "short_release":
            self.add_to_button_history(button)
            if button == "on":
                if self.is_quadruple_press(button):
                    if self.on_quadruple_press_function is not None:
                        self.on_quadruple_press_function()
                    else:
                        self.on_short_press_function()
                elif self.is_tripple_press(button):
                    if self.on_tripple_press_function is not None:
                        self.on_tripple_press_function()
                    else:
                        self.on_short_press_function()
                elif self.is_double_press(button):
                    if self.on_double_press_function is not None:
                        self.on_double_press_function()
                    else:
                        self.on_short_press_function()
                else:
                    if self.on_short_press_function is not None:
                        self.on_short_press_function()
            elif button == "up":
                if self.is_quadruple_press(button):
                    if self.up_quadruple_press_function is not None:
                        self.up_quadruple_press_function()
                    else:
                        self.up_short_press_function()
                elif self.is_tripple_press(button):
                    if self.up_tripple_press_function is not None:
                        self.up_tripple_press_function()
                    else:
                        self.up_short_press_function()
                elif self.is_double_press(button):
                    if self.up_double_press_function is not None:
                        self.up_double_press_function()
                    else:
                        self.up_short_press_function()
                else:
                    if self.up_short_press_function is not None:
                        self.up_short_press_function()
            elif button == "down":
                if self.is_quadruple_press(button):
                    if self.down_quadruple_press_function is not None:
                        self.down_quadruple_press_function()
                    else:
                        self.down_short_press_function()
                elif self.is_tripple_press(button):
                    if self.down_tripple_press_function is not None:
                        self.down_tripple_press_function()
                    else:
                        self.down_short_press_function()
                elif self.is_double_press(button):
                    if self.down_double_press_function is not None:
                        self.down_double_press_function()
                    else:
                        self.down_short_press_function()
                else:
                    if self.down_short_press_function is not None:
                        self.down_short_press_function()
            elif button == "off":
                if self.is_quadruple_press(button):
                    if self.off_quadruple_press_function is not None:
                        self.off_quadruple_press_function()
                    else:
                        self.off_short_press_function()
                elif self.is_tripple_press(button):
                    if self.off_tripple_press_function is not None:
                        self.off_tripple_press_function()
                    else:
                        self.off_short_press_function()
                elif self.is_double_press(button):
                    if self.off_double_press_function is not None:
                        self.off_double_press_function()
                    else:
                        self.off_short_press_function()
                else:
                    if self.off_short_press_function is not None:
                        self.off_short_press_function()

        if event == "repeat":
            self.repeat_counter += 1
            if button == "on":
                if self.on_hold_function is not None:
                    self.on_hold_function()
                if self.on_long_press_function is not None and self.repeat_counter == self.long_press_duration:
                    self.on_long_press_function()
            elif button == "up":
                if self.up_hold_function is not None:
                    self.up_hold_function()
                if self.up_long_press_function is not None and self.repeat_counter == self.long_press_duration:
                    self.up_long_press_function()
            elif button == "down":
                if self.down_hold_function is not None:
                    self.down_hold_function()
                if self.down_long_press_function is not None and self.repeat_counter == self.long_press_duration:
                    self.down_long_press_function()
            elif button == "off":
                if self.off_hold_function is not None:
                    self.off_hold_function()
                if self.off_long_press_function is not None and self.repeat_counter == self.long_press_duration:
                    self.off_long_press_function()

    def button_recently_pressed(self):
        if not self.button_history:
            return False
        return time.time() - [b["timestamp"] for b in self.button_history][-1] < 5.0

class ButtonHandler():
    def __init__(self, room):
        self.room = room
        self.master_bri = _phue.get_bri(MASTER_NAME[self.room])
        self.master_ct = _phue.get_ct(MASTER_NAME[self.room])
        self.current_scene = None
        self.find_closest_scene()

    def find_closest_scene(self):
        def difference(scene):
            scene_bri = float(data.get_scene(scene, self.room)[MASTER_NAME[self.room]]["bri"])
            scene_ct = float(data.get_scene(scene, self.room)[MASTER_NAME[self.room]]["ct"])
            bri_diff = abs(self.master_bri - scene_bri)
            ct_diff = abs(self.master_ct - scene_ct)
            return bri_diff + ct_diff

        self.current_scene = min(data.all_scenes, key=difference)
        log("current scene in %s: %s" % (self.room, self.current_scene))

    def update_current_scene(self, bri=None, ct=None):
        if bri is not None:
            self.master_bri = bri
        if ct is not None:
            self.master_ct = ct
        self.find_closest_scene()

    def __step(self, step):
        index = data.all_scenes.index(self.current_scene)
        index += step
        index = max(0, index)
        index = min(index, len(data.all_scenes) - 1)
        scene.transition(data.all_scenes[index], rooms=self.room)
        self.current_scene = data.all_scenes[index]
    
    def step_up(self):
        self.__step(1)
        log("stepping up in %s to %s" % (self.room, self.current_scene))

    def step_down(self):
        self.__step(-1)
        log("stepping down in %s to %s" % (self.room, self.current_scene))

def run_detached_shell(command):
    full_command = f"( (nohup {command} > /dev/null 2> /dev/null < /dev/null) & )"
    subprocess.Popen(full_command, shell=True, executable="/bin/bash")


turn_on_roomba_when_door_opens_until_time = -float('inf')


def start_roomba_now():
    global turn_on_roomba_when_door_opens_until_time
    turn_on_roomba_when_door_opens_until_time = -float('inf')
    log("starting roomba now")
    run_detached_shell("/home/pi/Programming/roomba/roomba.py --force-start")


switches = {r: Switch() for r in data.get_rooms()}
handlers = {r: ButtonHandler(r) for r in data.get_rooms()}


def _on_short_press(room, update_master):
    log(f"{room} on short press")
    s = scheduled_scene.transition(rooms=room)
    bri = s[MASTER_NAME[room]]["bri"]
    ct = s[MASTER_NAME[room]]["ct"]
    handlers[room].update_current_scene(bri=bri, ct=ct)
    if update_master:
        for sensor in all_sensors:
            sensor.set_master_bri(bri, time=.4)
            sensor.set_master_ct(ct, time=.4)

def _on_double_press(room):
    log(f"{room} on double press")
    scheduled_scene.transition(rooms=["arbeitszimmer"])

def _on_tripple_press(room):
    log(f"{room} on tripple press")
    scheduled_scene.transition(rooms=["kinderzimmer", "schlafzimmer"])

def _up_short_press(room):
    log(f"{room} up short press")
    handlers[room].step_up()

def _down_short_press(room):
    log(f"{room} down short press")
    handlers[room].step_down()

def _off_short_press(room):
    log(f"{room} off short press")
    scene.transition(name="off", rooms=room)
    handlers[room].update_current_scene(bri=0.0, ct=1.0)

def _off_double_press(room):
    log(f"{room} off double press")
    scene.transition(name="off")

def _off_tripple_press(room):
    log(f"{room} off tripple press")
    global turn_on_roomba_when_door_opens_until_time
    turn_on_roomba_when_door_opens_until_time = time.time() + 2 * 60 * 60

def _off_quadruple_press(room):
    log(f"{room} off quadruple press")
    start_roomba_now()

def _on_long_press(room):
    log(f"{room} on long press")
    run_detached_shell(f"/home/pi/Programming/huecontrol/wakeup.py -{room[0]} -t2 1m")

def _off_long_press(room, time, scene_name="off"):
    log(f"{room} off long press")
    scene.transition(name=scene_name, rooms=room, time=time)


for r in data.get_rooms():
    if r == "wohnzimmer":
        switches[r].set_on_short_press_function(lambda room=r: _on_short_press(room, update_master=True))
    else:
        switches[r].set_on_short_press_function(lambda room=r: _on_short_press(room, update_master=False))
    switches[r].set_up_short_press_function(lambda room=r: _up_short_press(room))
    switches[r].set_down_short_press_function(lambda room=r: _down_short_press(room))
    switches[r].set_off_short_press_function(lambda room=r: _off_short_press(room))
    switches[r].set_on_long_press_function(lambda room=r: _on_long_press(room))

switches["wohnzimmer"].set_off_double_press_function(lambda: _off_double_press("wohnzimmer"))
switches["wohnzimmer"].set_off_tripple_press_function(lambda: _off_tripple_press("wohnzimmer"))
switches["wohnzimmer"].set_off_quadruple_press_function(lambda: _off_quadruple_press("wohnzimmer"))

switches["wohnzimmer"].set_on_double_press_function(lambda: _on_double_press("wohnzimmer"))
switches["wohnzimmer"].set_on_tripple_press_function(lambda: _on_tripple_press("wohnzimmer"))

switches["wohnzimmer"].set_off_long_press_function(lambda: _off_long_press("wohnzimmer", 60*60))
switches["schlafzimmer"].set_off_long_press_function(lambda: _off_long_press("schlafzimmer", 3*60))
switches["kinderzimmer"].set_off_long_press_function(lambda: _off_long_press("kinderzimmer", 15*60, scene_name="min"))
switches["arbeitszimmer"].set_off_long_press_function(lambda: _off_long_press("arbeitszimmer", 60*60))


class MotionSensor():
    def __init__(self,
                 sensor_ids,
                 lights,
                 idle_timeout,
                 fade_off_time=20.0,
                 minimum_bri=None,
                 maximum_bri=1.0,
                 minimum_ct=0.3,
                 maximum_ct=1.0,
                 bri_masks=dict(),
                 use_ambient_for_brightness=False,
                 use_ambient_for_motion=False,
                 sensor_minimum_bri=dict()):

        self.sensor_ids = sensor_ids
        self.lights = lights
        self.idle_timeout = idle_timeout

        if minimum_bri is None:
            self.minimum_bri = _phue.min_bri()
        else:
            self.minimum_bri = minimum_bri
        self.maximum_bri = maximum_bri
        self.minimum_ct = minimum_ct
        self.maximum_ct = maximum_ct
        self.bri_masks = bri_masks
        self.fade_off_time = fade_off_time
        self.sensor_minimum_bri = sensor_minimum_bri

        self.use_ambient_for_brightness = use_ambient_for_brightness
        self.use_ambient_for_motion = use_ambient_for_motion

        self.master_bri = _phue.get_bri(MASTER_NAME["wohnzimmer"])
        self.master_ct = _phue.get_ct(MASTER_NAME["wohnzimmer"])
        self.ambient_bri = ambient.get_simulated_bri()  # uses history
        self.ambient_ct = None
        self.update_ambient_ct(update_lights=False)

        self.is_on = _phue.get_on(self.lights[0])
        if self.is_on:
            self.current_bri = _phue.get_bri(self.lights[0])
            self.current_ct = _phue.get_ct(self.lights[0])
        else:
            self.current_bri = float('nan')
            self.current_ct = float('nan')

        self.motion_detected = {s: False for s in self.sensor_ids}

    def is_this_sensor(self, sensor_id):
        return sensor_id in self.sensor_ids

    def get_sensor_ids(self):
        return self.sensor_ids

    def get_idle_timeout(self):
        return self.idle_timeout

    def using_ambient_values(self):
        return self.master_bri < self.ambient_bri - .02 and self.use_ambient_for_brightness

    def get_slave_bri(self):
        if self.using_ambient_values():
            ret = self.ambient_bri
        else:
            minimum_bri = self.minimum_bri
            if self.use_ambient_for_motion and ambient.get_schmitt_trigger():
                minimum_bri = 0.0
            ret = toolbox.map(self.master_bri, 0.0, 1.0, minimum_bri, self.maximum_bri)

        motion_active_sensors = [id for id, detected in self.motion_detected.items() if detected]
        for m in motion_active_sensors:
            if m in self.sensor_minimum_bri:
                ret = max(ret, self.sensor_minimum_bri[m])

        return ret

    def get_slave_ct(self):
        if self.using_ambient_values() and self.master_bri < .01:
            return self.ambient_ct
        return toolbox.map(self.master_ct, 0.0, 1.0, self.minimum_ct, self.maximum_ct)

    def lights_within_margin(self, bri=None, ct=None):
        if isnan(self.current_bri) or isnan(self.current_ct):
            return False

        if bri is not None:
            if .3 < bri:
                bri_margin = .05
            elif .05 < bri:
                bri_margin = .02
            else:
                bri_margin = _phue.min_bri()

            if bri_margin < abs(self.current_bri - bri):
                return False
        if ct is not None:
            ct_margin = .05
            if ct_margin < abs(self.current_ct - ct):
                return False
        return True
    
    def set_lights(self, bri=None, ct=None, time=None):
        if bri is None:
            bri = self.get_slave_bri()
        if ct is None:
            ct = self.get_slave_ct()
        log("set_lights", self.lights, "bri=%.2f, ct=%.2f" % (bri, ct))

        if time is None:
            time = 0.4
            if scene.transition_in_progress('wohnzimmer'):
                time = 60.0

        if self.bri_masks:
            non_mask_lights = [l for l in self.lights if l not in self.bri_masks]
            mask_lights = [l for l in self.lights if l in self.bri_masks]
            for l in mask_lights:
                _phue.set_lights(l, bri=self.bri_masks[l](bri), ct=ct, time=time)
            _phue.set_lights(non_mask_lights, bri=bri, ct=ct, time=time)
        else:
            _phue.set_lights(self.lights, bri=bri, ct=ct, time=time)
        self.current_bri = bri
        self.current_ct = ct

    def turn_off_lights(self):
        _phue.set_lights(self.lights, on=False, time=self.fade_off_time)
        self.current_bri = float('nan')
        self.current_ct = float('nan')

    def mark_motion_detected(self, sensor_id):
        log("mark_motion_detected " + sensor_id)
        self.motion_detected[sensor_id] = True

        bri = self.get_slave_bri()
        ct = self.get_slave_ct()
        self.is_on = True

        if not self.lights_within_margin(bri, ct):
            self.set_lights(bri, ct, time=.4)
    
    def mark_motion_idle_timeout(self, sensor_id):
        log("mark_motion_idle_timeout " + sensor_id)
        self.motion_detected[sensor_id] = False

        if not any(self.motion_detected.values()) and self.is_on:
            log("no motion detected, turning off lights", self.lights)
            self.is_on = False
            self.turn_off_lights()

    def set_master_bri(self, master_bri, time=None):
        log(f"set_master_bri {master_bri:.3g}")
        self.master_bri = master_bri
        bri = self.get_slave_bri()
        if not self.lights_within_margin(bri=bri) and self.is_on:
            self.set_lights(bri=bri, time=time)

    def set_master_ct(self, master_ct, time=None):
        log(f"set_master_ct {master_ct:.3g}")
        self.master_ct = master_ct
        ct = self.get_slave_ct()
        if not self.lights_within_margin(ct=ct) and self.is_on:
            self.set_lights(ct=ct, time=time)

    def update_lights(self, time=None):
        bri = self.get_slave_bri()
        ct = self.get_slave_ct()
        if not self.lights_within_margin(bri=bri, ct=ct) and self.is_on:
            self.set_lights(bri=bri, ct=ct, time=time)

    def set_ambient_bri(self, bri):
        log(f"set_ambient_bri {bri:.3g}")
        self.ambient_bri = bri
        self.update_lights(time=5*60)

    def update_ambient_ct(self, update_lights=True):
        d, _ = scheduled_scene.get_scene_dict()
        ct = d[MASTER_NAME["wohnzimmer"]]["ct"]
        ct = toolbox.map(ct, 1.0, 0.0, self.maximum_ct, self.minimum_ct)
        log(f"update_ambient_ct {ct:.3g}")
        self.ambient_ct = ct
        if update_lights:
            self.update_lights()


kuche_sensor = MotionSensor(sensor_ids=["9b8f4c05-d103-4fd9-930c-5ba824ae8f45"],
                            lights=data.get_lights("kuche"),
                            idle_timeout=10*60,
                            use_ambient_for_brightness=True)
all_sensors.append(kuche_sensor)


def flurlampe_mask(master):
    max_kinderzimmer_bri = max([global_brightness_values[k] for k in data.get_lights("kinderzimmer")])
    max_schlafzimmer_bri = max([global_brightness_values[k] for k in data.get_lights("schlafzimmer")])
    min_rooms = min(max_kinderzimmer_bri, max_schlafzimmer_bri, master)
    max_ambient = max(min_rooms, global_ambient_value)

    allow_off = (
        handlers["wohnzimmer"].current_scene == "off"
        and handlers["schlafzimmer"].current_scene == "off"
        and handlers["arbeitszimmer"].current_scene == "off"
        and (
            handlers["kinderzimmer"].current_scene == "off"
            or handlers["kinderzimmer"].current_scene == "min"
        )
    )

    if allow_off:
        ret = max_ambient
    else:
        ret = max(max_ambient, _phue.min_bri())

    log(
        f"flurlampe mask: "
        f"master={master:.3g}, "
        f"max_kinderzimmer_bri={max_kinderzimmer_bri:.3g}, "
        f"max_schlafzimmer_bri={max_schlafzimmer_bri:.3g}, "
        f"min_rooms={min_rooms:.3g}, "
        f"global_ambient_value={global_ambient_value:.3g}, "
        f"max_ambient={max_ambient:.3g}, "
        f"allow_off={allow_off}, "
        f"ret={ret:.3g}"
    )

    return ret


flur_sensor = MotionSensor(sensor_ids=["dc49cc1e-0253-495e-896c-11531913ef23"],
                           lights=data.get_lights("flur"),
                           idle_timeout=90,
                           bri_masks={"Flurlampe": flurlampe_mask},
                           use_ambient_for_brightness=True)
all_sensors.append(flur_sensor)


bad_sensor = MotionSensor(sensor_ids=["dd4b1e47-1e63-477c-b3c6-544048d5c8e1"],
                         lights=data.get_lights("bad"),
                         idle_timeout=15*60,
                         use_ambient_for_brightness=True)
all_sensors.append(bad_sensor)


diele_sensor = MotionSensor(sensor_ids=["ec5fe5f9-be48-4957-b37d-8ca3d2e1116a",
                                        "3482ecac-1562-413a-b519-46ec7b5e5883"],
                            lights=data.get_lights("diele"),
                            idle_timeout=5*60,
                            use_ambient_for_brightness=True,
                            sensor_minimum_bri={"3482ecac-1562-413a-b519-46ec7b5e5883":
                                                data.all_scene_attributes["gemutlich"]["bri"]})
all_sensors.append(diele_sensor)


klo_sensor = MotionSensor(sensor_ids=["96d931b2-ec53-4753-995a-129ee480d3d6"],
                          lights=data.get_lights("klo"),
                          idle_timeout=15*60,
                          use_ambient_for_brightness=True)
all_sensors.append(klo_sensor)


def get_sensor_object(sensor_id):
    for sensor in all_sensors:
        if sensor.is_this_sensor(sensor_id):
            return sensor
    raise ValueError(f"invalid sensor id: {sensor_id}")


last_file_mtime_bri = 0
last_file_mtime_ct = 0

try:
    with open("/home/pi/turn_off_lights_when_door_opens", "r") as f:
        content = f.read().strip()
        start_time, end_time = content.split("-")
        start_hour, start_minute = [int(x) for x in start_time.split(":")]
        end_hour, end_minute = [int(x) for x in end_time.split(":")]

    def turn_off_lights_when_door_opens():
        now = datetime.datetime.now().time()
        start = datetime.time(start_hour, start_minute)
        end = datetime.time(end_hour, end_minute)
        return start <= now <= end

    log(f"turn off lights when door opens: {start_hour}:{start_minute:02d} - {end_hour}:{end_minute:02d}")

except Exception as e:
    log(f"error reading turn_off_lights_when_door_opens: {e}")

    def turn_off_lights_when_door_opens():
        return False


async def main():
    # Connect to the Hue Bridge
    bridge = HueBridgeV2(ip_address, app_key=user_id)
    await bridge.initialize()
    log("Connected to the Hue Bridge.")

    async def periodic_update():
        while True:
            for sensor in all_sensors:
                await asyncio.sleep(5 * 60)
                sensor.update_ambient_ct()
    periodic_update_task = asyncio.create_task(periodic_update())

    # Function to handle timeout after no motion is detected for 60 seconds
    async def motion_timeout(sensor_id, timeout):
        await asyncio.sleep(timeout)
        #log(f"No motion detected for {timeout} seconds on sensor {sensor_id}.")
        sensor = get_sensor_object(sensor_id)
        sensor.mark_motion_idle_timeout(sensor_id)

    try:
        motion_sensors_ids = list()
        for sensor in all_sensors:
            motion_sensors_ids.extend(sensor.get_sensor_ids())

        # Identify motion sensors by checking ResourceTypes.MOTION
        #motion_sensors_ids = [
        #    sensor.id for sensor in bridge.sensors
        #    if sensor.type == ResourceTypes.MOTION
        #]

        #if not motion_sensors_ids:
        #    log("No motion sensors found.")
        #    return

        motion_timeout_tasks = dict()

        #log("Detected motion sensors:")
        #for sensor_id in motion_sensors_ids:
        #    log(f"Sensor ID: {sensor_id}")

        # create motion timeout tasks for all motion sensors
        # start them now to define motion just ended on all sensors
        for sensor_id in motion_sensors_ids:
            sensor_object = get_sensor_object(sensor_id)
            motion_timeout_tasks[sensor_id] = asyncio.create_task(
                motion_timeout(sensor_id, sensor_object.get_idle_timeout())
            )

        # Define a callback function for processing motion events
        async def handle_event(event_type, event):
            try:
                await _handle_event(event_type, event)
            except Exception as e:
                traceback.print_exc()
                os._exit(1)

        async def _handle_event(event_type, event):
            global global_ambient_value

            # log(event)
            if event is None:
                return

            if event["type"] == "grouped_light":
                # no idea what this is but it has ids that cant be found by light_ids.get_name(), so ignore
                return

            if "on" in event:
                name = light_ids.get_name(event["id"])
                global_on_values[name] = event["on"]["on"]

            if "dimming" in event:
                name = light_ids.get_name(event["id"])
                if not global_on_values[name]:
                    # when turning off lights in apple home app it only writes to on
                    # and doesnt override the bri value. that means if there is a transition
                    # ongoing and you turn it off, you keep getting events of the transition.
                    # so we need to to ignore these events.
                    return

            if event['id'] == BALCONY_MOTION_SENSOR:
                # only used for ambient data not as motion sensor
                return

            if "dimming" in event:
                name = light_ids.get_name(event["id"])
                if name is not None:
                    bri = event["dimming"]["brightness"] / 100.0
                    global_brightness_values[name] = bri

            if "on" in event:
                name = light_ids.get_name(event["id"])
                if name is not None:
                    if event['on']['on'] == False:
                        global_brightness_values[name] = 0.0

            # Handle dimming events
            if event["id"] in MASTER_ID.values():
                room = [r for r, id in MASTER_ID.items() if id == event["id"]][0]
                if not _phue.fake_recently_changed() or room != "wohnzimmer":
                    if "dimming" in event:
                        brightness = event["dimming"]["brightness"]
                        if not switches[room].button_recently_pressed():
                            handlers[room].update_current_scene(bri=brightness / 100.0)
                        if room == "wohnzimmer":
                            for sensor in all_sensors:
                                sensor.set_master_bri(brightness / 100.0)

                    if "on" in event:
                        if event['on']['on'] == False:
                            if not switches[room].button_recently_pressed():
                                handlers[room].update_current_scene(bri=0.0, ct=1.0)
                            if room == "wohnzimmer":
                                for sensor in all_sensors:
                                    sensor.set_master_bri(0.0)

                    if "color_temperature" in event:
                        if event["color_temperature"]["mirek_valid"]:
                            mirek = event["color_temperature"]["mirek"]
                            ct = _phue.convert_mirek_to_ct(mirek)
                            if not switches[room].button_recently_pressed():
                                handlers[room].update_current_scene(ct=ct)
                            if room == "wohnzimmer":
                                for sensor in all_sensors:
                                    sensor.set_master_ct(ct)
                        else:
                            log("mirek not valid:", event)

            # Handle light level events
            if event['type'] == "light_level":
                if event['id'] == AMBIENT_SENSOR_ID:
                    light_level = event['light']['light_level']
                    bri = ambient.convert_sensor_value_to_bri(light_level)
                    for sensor in all_sensors:
                        sensor.set_ambient_bri(bri)
                    global_ambient_value = bri
                    # log(f"Light level changed: {light_level}")

            # Handle motion events
            if event["type"] == "motion" or event["type"] == "contact":
                #log("motion event", event)

                sensor_id = event['id']

                if sensor_id not in motion_sensors_ids:
                    log("sensor id not known:", sensor_id, event)
                    return

                sensor = get_sensor_object(sensor_id)

                if event['type'] == 'motion':
                    on = event['motion']['motion']
                elif event['type'] == 'contact':
                    on = event['contact_report']['state'] == 'no_contact'

                if on:
                    #log(f"Motion detected from sensor {sensor_id}")
                    sensor.mark_motion_detected(sensor_id)

                    # Cancel the current timeout task for this sensor if it exists
                    nonlocal motion_timeout_tasks

                    task = motion_timeout_tasks[sensor_id]
                    if task is not None and not task.done():
                        task.cancel()
                        try:
                            await task
                        except asyncio.CancelledError:
                            pass
                    motion_timeout_tasks[sensor_id] = None

                else:
                    # Schedule a timeout task for this sensor
                    idle_timeout = sensor.get_idle_timeout()
                    motion_timeout_tasks[sensor_id] = asyncio.create_task(motion_timeout(sensor_id, idle_timeout))

            if "button" in event:
                button_id = event['id']
                event_type = event['button']['button_report']['event']
                
                log(button_id, event_type)
                room, button = data.buttons[button_id]
                log(room, button)
                switches[room].button_event(button, event_type)

            if event["id"] == "3482ecac-1562-413a-b519-46ec7b5e5883":
                if event['contact_report']['state'] == 'no_contact':
                    if turn_off_lights_when_door_opens():
                        scene.transition(name="off", rooms=["wohnzimmer", "arbeitszimmer"])
                        log("wohnzimmer, arbeitszimmer off triggered by door")
                    if time.time() < turn_on_roomba_when_door_opens_until_time:
                        start_roomba_now()


        # Subscribe to events
        log("Listening for events...")
        bridge.events.subscribe(handle_event)

        # Keep the script running to listen for events
        while True:
            await asyncio.sleep(1)

    finally:
        # Ensure the client session is closed
        await bridge.close()


if __name__ == "__main__":
    asyncio.run(main())
