#!/usr/bin/python3
import datetime
import schedule
import scene
import toolbox
import data
import argparse
from time import sleep


def __get_last_two_variables(dt=None):
    definitions = schedule.get_variable_definitions()
    definitions = [d for d in definitions if d.when <= dt]
    definitions = [d for d in definitions if d.variable == "scheduled_scene"]
    for d in definitions[-2:]:
        if d.scene_args is None:
            d.scene_args = lambda: None
            d.scene_args.time = 0.0
    current = definitions[-1]
    before = definitions[-2]
    return current, before


def get_data(scene_name, wohnzimmer=True, schlafzimmer=True):
    if wohnzimmer and schlafzimmer:
        return getattr(data, scene_name)
    elif wohnzimmer:
        return getattr(data, scene_name + "_wohnzimmer")
    elif schlafzimmer:
        return getattr(data, scene_name + "_schlafzimmer")
    else:
        raise RuntimeError('no room selected')


def get_scene_dict(dt=None, wohnzimmer=True, schlafzimmer=True):
    if dt is None:
        dt = datetime.datetime.now()

    current, before = __get_last_two_variables(dt)

    transition_start = current.when
    transition_end = current.when + datetime.timedelta(seconds=current.scene_args.time)
    transition_start = transition_start.timestamp()
    transition_end = transition_end.timestamp()

    if .1 < current.scene_args.time:
        f = toolbox.map(dt.timestamp(), transition_start, transition_end, 0, 1, clamp=True)
        adjusted_transition_time = transition_end - dt.timestamp()
        s = toolbox.scene_superposition(f, get_data(current.value, wohnzimmer=wohnzimmer, schlafzimmer=schlafzimmer),
                                        1 - f, get_data(before.value, wohnzimmer=wohnzimmer, schlafzimmer=schlafzimmer))
        return s, adjusted_transition_time
    else:
        return get_data(current.value, wohnzimmer=wohnzimmer, schlafzimmer=schlafzimmer), 0.0


def parse_args(input_args=None):
    if isinstance(input_args, str):
        input_args = input_args.split()
        this_file = __file__.split("/")[-1].removesuffix(".py")
        if input_args[0].startswith(this_file):
            input_args = input_args[1:]

    parser = argparse.ArgumentParser()
    parser.add_argument('-t', type=str, default='0.4s', dest='time')
    parser.add_argument('-w', action='store_true', dest='wohnzimmer')
    parser.add_argument('-s', action='store_true', dest='schlafzimmer')
    args = parser.parse_args(input_args if input_args else None)
    args.time = toolbox.convert_time_string(args.time)
    if not args.wohnzimmer and not args.schlafzimmer:
        args.wohnzimmer = True
        args.schlafzimmer = True
    return args


def transition_schlafzimmer(time=.4):
    transition(time=time, wohnzimmer=False, schlafzimmer=True)


def transition_wohnzimmer(time=.4):
    transition(time=time, wohnzimmer=True, schlafzimmer=False)


def transition(time=.4, wohnzimmer=True, schlafzimmer=True, hour=None, minute=None, dt=None):
    if dt is None:
        dt = datetime.datetime.now()
    dt = dt.replace(second=0, microsecond=0)
    if hour is not None:
        dt = dt.replace(hour=hour)
    if minute is not None:
        dt = dt.replace(minute=minute)

    current, _ = __get_last_two_variables(dt)

    if current.when + datetime.timedelta(seconds=(current.scene_args.time-60)) < dt:
        scene.transition_dicionary(get_data(current.value, wohnzimmer, schlafzimmer), time=time)
    else:
        s, adjusted_transition_time = get_scene_dict(dt, wohnzimmer=wohnzimmer, schlafzimmer=schlafzimmer)
        scene.transition_dicionary(s)
        sleep(1.0 + time)
        adjusted_transition_time -= 60  # to not run into next transition
        adjusted_transition_time = max(adjusted_transition_time, .4)
        scene.transition_dicionary(get_data(current.value, wohnzimmer=wohnzimmer, schlafzimmer=schlafzimmer),
                                   time=adjusted_transition_time)


def main(input_args=None):
    args = parse_args(input_args)
    transition(time=args.time, wohnzimmer=args.wohnzimmer, schlafzimmer=args.schlafzimmer)


if __name__ == '__main__':
    main()

