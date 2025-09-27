def convert_time_string(time_str):
    unit_is_minutes = False
    if time_str.endswith("m"):
        unit_is_minutes = True
        time_str = time_str[:-1]
    if time_str.endswith("s"):
        time_str = time_str[:-1]
    time = float(time_str.replace(",", "."))
    if unit_is_minutes:
        time *= 60
    return time


def map(x, in_min, in_max, out_min, out_max, clamp=False):
    ret = (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    if clamp:
        lower, higher = sorted([out_min, out_max])
        ret = min(higher, ret)
        ret = max(lower, ret)
    return ret


def scene_superposition(factor1, scene1, factor2, scene2):
    lamps1 = set(scene1.keys())
    lamps2 = set(scene2.keys())
    if not lamps1 == lamps2:
        raise RuntimeError('scene_superposion: different lamps in scenes')
    for l in lamps1:
        properties1 = set(scene1[l].keys())
        properties2 = set(scene2[l].keys())
        if not properties1 == properties2:
            raise RuntimeError(f'secen_superposition: different properies for lamp {l}')

    ret = dict()
    for l in lamps1:
        ret[l] = dict()
        for p in set(scene1[l].keys()):
            ret[l][p] = factor1 * scene1[l][p] + factor2 * scene2[l][p]
            if p == "on":
                ret[l][p] = bool(ret[l][p])
    return ret
