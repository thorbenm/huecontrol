import datetime
import schedule
import scene
import toolbox
import data
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


def get_scene_dict(dt=None):
    if dt is None:
        dt = datetime.datetime.now()

    current, before = __get_last_two_variables(dt)

    transition_start = current.when
    transition_end = current.when + datetime.timedelta(seconds=current.scene_args.time)
    transition_start = transition_start.timestamp()
    transition_end = transition_end.timestamp()

    if .1 < current.scene_args.time:
        f = toolbox.map(dt.timestamp(), transition_start, transition_end, 0, 1, clamp=True)
        transition_time = transition_end - dt.timestamp()
        s = toolbox.scene_superposition(f, getattr(data, current.value),
                                        1 - f, getattr(data, before.value))
        return s, transition_time
    else:
        return getattr(data, current.value), 0.0


def transition(time=.4, hour=None, minute=None, dt=None):
    if dt is None:
        dt = datetime.datetime.now()
    dt = dt.replace(second=0, microsecond=0)
    if hour is not None:
        dt = dt.replace(hour=hour)
    if minute is not None:
        dt = dt.replace(minute=minute)

    current, _ = __get_last_two_variables(dt)

    if current.when + datetime.timedelta(seconds=current.scene_args.time) < dt:
        scene.transition(current.value, time=time)
    else:
        s, transition_time = get_scene_dict(dt)
        scene.transition_dicionary(s)
        sleep(1.0 + time)
        scene.transition(current.value, time=transition_time)


def main():
    transition()


if __name__ == '__main__':
    main()

