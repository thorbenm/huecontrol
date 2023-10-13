def convert_time_string(time_str):
    unit_is_minutes = False
    if time_str.endswith("m"):
        unit_is_minutes = True
    time = float(time_str[:-1].replace(",", "."))
    if unit_is_minutes:
        time *= 60
    return time


def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
