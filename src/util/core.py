from json import dumps
from typing import Callable, Dict, TypeVar, List
import dpath
import pickle


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


T = TypeVar("T")


def some(arr: List[T], func: Callable[[T], bool]) -> bool:
    for item in arr:
        if func(item):
            return True
    return False


def dump_pickle(obj, fname):
    with open(fname, "wb") as f:
        pickle.dump(obj, f)


def load_pickle(fname):
    with open(fname, "rb") as f:
        return pickle.load(f)
