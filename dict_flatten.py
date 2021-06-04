import dataclasses


@dataclasses.dataclass
class LineData:
    key_path: tuple[str]
    new_indent: int
    key: str
    value: str


def get_lines(dct: dict, _key_path=None) -> list[LineData]:
    # (key_path, new_indent, key, value,)

    if _key_path is None:
        _key_path = []

    out = []
    for key, val in dct.items():
        if isinstance(val, dict):
            new_out = get_lines(val, _key_path + [key])
            if len(new_out):
                out.append(LineData(tuple(), 1, str(key), ''))
                out += new_out
                out[-1].new_indent -= 1
        else:
            out.append(LineData(tuple(_key_path + [key]), 0, str(key), str(val)))
    return out
