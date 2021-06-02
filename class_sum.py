import json


def sum_dicts(lst: list[dict]):
    out = {}
    if len(lst) == 0:
        return out

    for key, val in lst[0].items():
        if isinstance(val, list) and isinstance(val[0], dict):
            all_vals = [sum_dicts(a[key]) for a in lst]
        else:
            all_vals = [a[key] for a in lst]

        if isinstance(val, dict):
            out[key] = sum_dicts(all_vals)
        else:
            try:
                out[key] = sum(all_vals)
            except TypeError:
                pass
    return out


def sum_classes(lst: list):
    out_dict = json_dump_load(dict(lst), default=lambda o: o.__dict__)
    return sum_dicts(list(out_dict.values()))


def json_dump_load(x: dict, **kwargs) -> dict:
    return json.loads(json.dumps(x, **kwargs))
