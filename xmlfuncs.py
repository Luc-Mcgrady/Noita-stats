import xml_python


def as_attr_dict(entry: xml_python.Element):
    out = entry.attrib
    for item in entry:
        suffix = ''  # Suffixes so we don't overwrite elements
        tag = item.tag

        if f"{tag}{suffix}" in out:
            suffix = 1
            while f"{tag}{suffix}" in out:
                suffix += 1

        out = {**out, f"{tag}{suffix}": as_attr_dict(item)}
    return out
