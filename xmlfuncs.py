import xml_python


def as_attr_dict(entry: xml_python.Element):
    out = entry.attrib
    for item in entry:
        tag = item.tag

        if tag in out:
            if type(out[tag]) != list:
                out[tag] = [out[tag]]
            out[tag].append(as_attr_dict(item))
        else:
            out = {**out, tag: as_attr_dict(item)}
    return out
