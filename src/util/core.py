from json import dumps
from typing import Dict
import dpath


def dump_to_file(s: str, fnmae: str, json=True):
    with open(fnmae, "w") as f:
        if json:
            f.write(dumps(s, indent=2))
        else:
            f.write(s)


def dget(d: Dict, path: str):
    try:
        return dpath.get(d, path)
    except KeyError:
        return None
