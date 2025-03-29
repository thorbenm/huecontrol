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


MASTER_NAME = {r: data.get_lights(r)[0] for r in ["wohnzimmer", "schlafzimmer", "kinderzimmer"]}
MASTER_ID = {r: light_ids.get_id(n) for r, n in MASTER_NAME.items()}
AMBIENT_SENSOR_ID = "9dd345e1-d99a-40eb-8cfd-25209e90ebfd"


def running_under_systemd():
    return os.environ.get('INVOCATION_ID') is not None


def log(*args, **kwargs):
    message = " ".join(str(arg) for arg in args)
    systemd.journal.write(message)
    if not running_under_systemd():
        print(message, **kwargs)


class Switch():
    def __init__(self, ):
        self.long_press_duration = 3
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

        self.last_event = -float('inf')

    def set_on_short_press_function(self, f):
        self.on_short_press_function = f

    def set_up_short_press_function(self, f):
        self.up_short_press_function = f

    def set_down_short_press_function(self, f):
        self.down_short_press_function = f

    def set_off_short_press_function(self, f):
        self.off_short_press_function = f

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
        self.last_event = time.time()

        if event != "repeat":
            self.repeat_counter = 0

        if event == "short_release":
            if button == "on":
                if self.on_short_press_function is not None:
                    self.on_short_press_function()
            elif button == "up":
                if self.up_short_press_function is not None:
                    self.up_short_press_function()
            elif button == "down":
                if self.down_short_press_function is not None:
                    self.down_short_press_function()
            elif button == "off":
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
        return time.time() - self.last_event < 5.0

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
        scene.transition(data.all_scenes[index], room=self.room)
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


wbh = ButtonHandler("wohnzimmer")
wohnzimmer_switch = Switch()

def wohnzimmer_on_short_press():
    log("wohnzimmer on short press")
    s = scheduled_scene.transition(room="wohnzimmer")
    bri = s[MASTER_NAME["wohnzimmer"]]["bri"]
    ct = s[MASTER_NAME["wohnzimmer"]]["ct"]
    wbh.update_current_scene(bri=bri, ct=ct)

def wohnzimmer_up_short_press():
    log("wohnzimmer up short press")
    wbh.step_up()

def wohnzimmer_down_short_press():
    log("wohnzimmer down short press")
    wbh.step_down()

def wohnzimmer_off_short_press():
    log("wohnzimmer off short press")
    scene.transition(name="off", room="wohnzimmer")
    wbh.update_current_scene(bri=0.0, ct=1.0)

def wohnzimmer_on_long_press():
    log("wohnzimmer on long press")
    run_detached_shell("/home/pi/Programming/huecontrol/wakeup.py -w -t2 3m")

def wohnzimmer_off_long_press():
    log("wohnzimmer off long press")
    scene.transition(name="off", room="wohnzimmer", time=30*60)

wohnzimmer_switch.set_on_short_press_function(wohnzimmer_on_short_press)
wohnzimmer_switch.set_up_short_press_function(wohnzimmer_up_short_press)
wohnzimmer_switch.set_down_short_press_function(wohnzimmer_down_short_press)
wohnzimmer_switch.set_off_short_press_function(wohnzimmer_off_short_press)
wohnzimmer_switch.set_on_long_press_function(wohnzimmer_on_long_press)
wohnzimmer_switch.set_off_long_press_function(wohnzimmer_off_long_press)


sbh = ButtonHandler("schlafzimmer")
schlafzimmer_switch = Switch()

def schlafzimmer_on_short_press():
    log("schlafzimmer bed on short press")
    s = scheduled_scene.transition(room="schlafzimmer")
    bri = s[MASTER_NAME["schlafzimmer"]]["bri"]
    ct = s[MASTER_NAME["schlafzimmer"]]["ct"]
    sbh.update_current_scene(bri=bri, ct=ct)

def schlafzimmer_up_short_press():
    log("schlafzimmer bed up short press")
    sbh.step_up()

def schlafzimmer_down_short_press():
    log("schlafzimmer bed down short press")
    sbh.step_down()

def schlafzimmer_off_short_press():
    log("schlafzimmer bed off short press")
    scene.transition(name="off", room="schlafzimmer")
    sbh.update_current_scene(bri=0.0, ct=1.0)

def schlafzimmer_on_long_press():
    log("schlafzimmer bed on long press")
    run_detached_shell("/home/pi/Programming/huecontrol/wakeup.py -s -t2 1m")

def schlafzimmer_off_long_press():
    log("schlafzimmer bed off long press")
    scene.transition(name="off", room="schlafzimmer", time=3*60)

schlafzimmer_switch.set_on_short_press_function(schlafzimmer_on_short_press)
schlafzimmer_switch.set_up_short_press_function(schlafzimmer_up_short_press)
schlafzimmer_switch.set_down_short_press_function(schlafzimmer_down_short_press)
schlafzimmer_switch.set_off_short_press_function(schlafzimmer_off_short_press)
schlafzimmer_switch.set_on_long_press_function(schlafzimmer_on_long_press)
schlafzimmer_switch.set_off_long_press_function(schlafzimmer_off_long_press)


kbh = ButtonHandler("kinderzimmer")
kinderzimmer_switch = Switch()

def kinderzimmer_on_short_press():
    log("kinderzimmer on short press")
    s = scheduled_scene.transition(room="kinderzimmer")
    bri = s[MASTER_NAME["kinderzimmer"]]["bri"]
    ct = s[MASTER_NAME["kinderzimmer"]]["ct"]
    kbh.update_current_scene(bri=bri, ct=ct)

def kinderzimmer_up_short_press():
    log("kinderzimmer up short press")
    kbh.step_up()

def kinderzimmer_down_short_press():
    log("kinderzimmer down short press")
    kbh.step_down()

def kinderzimmer_off_short_press():
    log("kinderzimmer off short press")
    scene.transition(name="off", room="kinderzimmer")
    kbh.update_current_scene(bri=0.0, ct=1.0)

def kinderzimmer_on_long_press():
    log("kinderzimmer on long press")
    run_detached_shell("/home/pi/Programming/huecontrol/wakeup.py -k -t2 1m")

def kinderzimmer_off_long_press():
    log("kinderzimmer off long press")
    scene.transition(name="off", room="kinderzimmer", time=3*60)

kinderzimmer_switch.set_on_short_press_function(kinderzimmer_on_short_press)
kinderzimmer_switch.set_up_short_press_function(kinderzimmer_up_short_press)
kinderzimmer_switch.set_down_short_press_function(kinderzimmer_down_short_press)
kinderzimmer_switch.set_off_short_press_function(kinderzimmer_off_short_press)
kinderzimmer_switch.set_on_long_press_function(kinderzimmer_on_long_press)
kinderzimmer_switch.set_off_long_press_function(kinderzimmer_off_long_press)


class MotionSensor():
    def __init__(self,
                 sensor_ids,
                 lights,
                 idle_timeout=120.0,
                 fade_off_time=20.0,
                 minimum_bri=None,
                 maximum_bri=1.0,
                 minimum_ct=0.3,
                 maximum_ct=1.0,
                 use_ambient_for_brightness=False,
                 use_ambient_for_motion=False):

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

        self.fade_off_time = fade_off_time

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
        return self.master_bri < self.ambient_bri and self.use_ambient_for_brightness

    def get_slave_bri(self):
        if self.using_ambient_values():
            return self.ambient_bri
        else:
            minimum_bri = self.minimum_bri
            if self.use_ambient_for_motion and ambient.get_schmitt_trigger():
                minimum_bri = 0.0
            return toolbox.map(self.master_bri, 0.0, 1.0, minimum_bri, self.maximum_bri)

    def get_slave_ct(self):
        if self.using_ambient_values():
            if 0.01 < self.master_bri:
                return self.master_ct
            else:
                return self.ambient_ct
        else:
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
    
    def set_lights(self, bri=None, ct=None, force_fast=False):
        if bri is None:
            bri = self.get_slave_bri()
        if ct is None:
            ct = self.get_slave_ct()
        log("set_lights", self.lights, "bri=%.2f, ct=%.2f" % (bri, ct))

        t = 0.4
        if not force_fast and scene.transition_in_progress('wohnzimmer'):
            t = 20.0

        _phue.set_lights(self.lights, bri=bri, ct=ct, time=t)
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
            self.set_lights(bri, ct, force_fast=True)
    
    def mark_motion_idle_timeout(self, sensor_id):
        log("mark_motion_idle_timeout " + sensor_id)
        self.motion_detected[sensor_id] = False

        if not any(self.motion_detected.values()) and self.is_on:
            log("no motion detected, turning off lights", self.lights)
            self.is_on = False
            self.turn_off_lights()

    def set_master_bri(self, master_bri):
        log("set_master_bri " + str(master_bri))
        self.master_bri = master_bri
        bri = self.get_slave_bri()
        if not self.lights_within_margin(bri=bri) and self.is_on:
            self.set_lights(bri=bri)

    def set_master_ct(self, master_ct):
        log("set_master_ct " + str(master_ct))
        self.master_ct = master_ct
        ct = self.get_slave_ct()
        if not self.lights_within_margin(ct=ct) and self.is_on:
            self.set_lights(ct=ct)

    def update_lights(self):
        bri = self.get_slave_bri()
        ct = self.get_slave_ct()
        if not self.lights_within_margin(bri=bri, ct=ct) and self.is_on:
            self.set_lights(bri=bri, ct=ct)

    def set_ambient_bri(self, bri):
        log("set_ambient_bri " + str(bri))
        self.ambient_bri = bri
        self.update_lights()

    def update_ambient_ct(self, update_lights=True):
        d, _ = scheduled_scene.get_scene_dict()
        ct = d[MASTER_NAME["wohnzimmer"]]["ct"]
        ct = toolbox.map(ct, 1.0, 0.0, self.maximum_ct, self.minimum_ct)
        log("update_ambient_ct " + str(ct))
        self.ambient_ct = ct
        if update_lights:
            self.update_lights()


all_sensors = list()


kuche_sensor = MotionSensor(sensor_ids=["96d931b2-ec53-4753-995a-129ee480d3d6"],
                           lights=data.get_lights("kuche"),
                           fade_off_time=120.0,
                           use_ambient_for_motion=True)
all_sensors.append(kuche_sensor)


flur_sensor = MotionSensor(sensor_ids=["ec5fe5f9-be48-4957-b37d-8ca3d2e1116a",
                                       "dc49cc1e-0253-495e-896c-11531913ef23"],
                           lights=data.get_lights("flur"),
                           use_ambient_for_brightness=True)
all_sensors.append(flur_sensor)


bad_sensor = MotionSensor(sensor_ids=["dd4b1e47-1e63-477c-b3c6-544048d5c8e1"],
                         lights=data.get_lights("bad"),
                         idle_timeout=15*60,
                         use_ambient_for_brightness=True)
all_sensors.append(bad_sensor)


def get_sensor_object(sensor_id):
    for sensor in all_sensors:
        if sensor.is_this_sensor(sensor_id):
            return sensor
    raise ValueError(f"invalid sensor id: {sensor_id}")


last_file_mtime_bri = 0
last_file_mtime_ct = 0

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
            #log(event)

            if event is None:
                return

            # Handle dimming events
            if event["id"] == MASTER_ID["wohnzimmer"]:
                if not _phue.fake_recently_changed():
                    if "dimming" in event:
                        brightness = event["dimming"]["brightness"]
                        #log("New master brightness:", brightness)
                        for sensor in all_sensors:
                            sensor.set_master_bri(brightness / 100.0)
                        if not wohnzimmer_switch.button_recently_pressed():
                            wbh.update_current_scene(bri=brightness / 100.0)

                    if "on" in event:
                        if event['on']['on'] == False:
                            for sensor in all_sensors:
                                sensor.set_master_bri(0.0)
                            if not wohnzimmer_switch.button_recently_pressed():
                                wbh.update_current_scene(bri=0.0, ct=1.0)

                    # handle color temperature events
                    if "color_temperature" in event:
                        if event["color_temperature"]["mirek_valid"]:
                            mirek = event["color_temperature"]["mirek"]
                            ct = _phue.convert_mirek_to_ct(mirek)
                            for sensor in all_sensors:
                                sensor.set_master_ct(ct)
                            if not wohnzimmer_switch.button_recently_pressed():
                                wbh.update_current_scene(ct=ct)
                        else:
                            log("mirek not valid:", event)

            if event["id"] == MASTER_ID["schlafzimmer"]:
                if "dimming" in event:
                    brightness = event["dimming"]["brightness"]
                    if not schlafzimmer_switch.button_recently_pressed():
                        sbh.update_current_scene(bri=brightness / 100.0)
                if "on" in event:
                    if event['on']['on'] == False:
                        if not schlafzimmer_switch.button_recently_pressed():
                            sbh.update_current_scene(bri=0.0, ct=1.0)
                if "color_temperature" in event:
                    if event["color_temperature"]["mirek_valid"]:
                        mirek = event["color_temperature"]["mirek"]
                        ct = _phue.convert_mirek_to_ct(mirek)
                        if not schlafzimmer_switch.button_recently_pressed():
                            sbh.update_current_scene(ct=ct)
                    else:
                        log("mirek not valid:", event)

            if event["id"] == MASTER_ID["kinderzimmer"]:
                if "dimming" in event:
                    brightness = event["dimming"]["brightness"]
                    if not kinderzimmer_switch.button_recently_pressed():
                        kbh.update_current_scene(bri=brightness / 100.0)
                if "on" in event:
                    if event['on']['on'] == False:
                        if not kinderzimmer_switch.button_recently_pressed():
                            kbh.update_current_scene(bri=0.0, ct=1.0)
                if "color_temperature" in event:
                    if event["color_temperature"]["mirek_valid"]:
                        mirek = event["color_temperature"]["mirek"]
                        ct = _phue.convert_mirek_to_ct(mirek)
                        if not kinderzimmer_switch.button_recently_pressed():
                            kbh.update_current_scene(ct=ct)
                    else:
                        log("mirek not valid:", event)

            # Handle light level events
            if event['type'] == "light_level":
                if event['id'] == AMBIENT_SENSOR_ID:
                    light_level = event['light']['light_level']
                    bri = ambient.convert_sensor_value_to_bri(light_level)
                    for sensor in all_sensors:
                        sensor.set_ambient_bri(bri)
                    # log(f"Light level changed: {light_level}")

            # Handle motion events
            if event['type'] == "motion":
                #log("motion event", event)
                sensor_id = event['id']

                if sensor_id not in motion_sensors_ids:
                    return

                sensor = get_sensor_object(sensor_id)
                motion_detected = event['motion']['motion']

                if motion_detected:
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
                button_names = {
                    '434e02f5-0679-47d8-afb7-7e74ba8b0f0a': ['wohnzimmer fridge', 'on'],
                    '9b85666c-ff81-4c8c-95d8-9034b74e9c57': ['wohnzimmer fridge', 'up'],
                    '2cdf8ceb-d272-44fb-ad7e-a9903045633a': ['wohnzimmer fridge', 'down'],
                    '86ccd746-e412-4089-81ab-882c4826bdaf': ['wohnzimmer fridge', 'off'],

                    '40d45630-a6a3-461c-bbb9-240788c87910': ['wohnzimmer door', 'on'],
                    '49b46ed1-a774-4656-8456-ec262b07a375': ['wohnzimmer door', 'up'],
                    'bdaf080a-e651-4e30-bfe6-1e169eb9b6f4': ['wohnzimmer door', 'down'],
                    '6133ace3-7a9e-4de8-a1a6-ec0f6bf9c3c4': ['wohnzimmer door', 'off'],

                    '5610d840-191e-4ebb-9087-1db469842897': ['schlafzimmer door', 'on'],
                    'cacdfa45-d676-4c3f-af87-e144c1036d86': ['schlafzimmer door', 'up'],
                    '772ca980-dbdf-4c09-854c-52cd0054835e': ['schlafzimmer door', 'down'],
                    '3105cbbd-9559-45f4-b470-591e75977014': ['schlafzimmer door', 'off'],
                    
                    '78a2ea22-6d24-44b8-8129-4628f8fc1486': ['schlafzimmer bed', 'on'],
                    '4583c212-827e-44aa-b89f-91312f8b5d1c': ['schlafzimmer bed', 'up'],
                    '42fc8925-9d12-4ee2-bcc9-daaa984689ec': ['schlafzimmer bed', 'down'],
                    'bed51e86-48ef-4e72-a6ac-732a2d149703': ['schlafzimmer bed', 'off'],

                    '7651940a-eadc-44b6-8757-75ac59df36bf': ['kinderzimmer', 'on'],
                    'c2fa050b-7c44-45db-9df7-53c9fb5f23c1': ['kinderzimmer', 'up'],
                    'da413bc1-b656-4679-a804-3a73e9ee146d': ['kinderzimmer', 'down'],
                    'be2ac1af-410c-426d-a673-fcabcd317b61': ['kinderzimmer', 'off'],
                }

                button_id = event['id']
                event_type = event['button']['button_report']['event']
                
                switch, button = button_names[button_id]
                if switch.startswith("wohnzimmer"):
                    wohnzimmer_switch.button_event(button, event_type)
                elif switch.startswith("schlafzimmer"):
                    schlafzimmer_switch.button_event(button, event_type)
                elif switch.startswith("kinderzimmer"):
                    kinderzimmer_switch.button_event(button, event_type)

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
