from typing import List, Tuple, TypedDict
from ..util import POS_TAGS
from ..type import Dependencies


class Entry(TypedDict):
    id: str
    text: str
    pos: POS_TAGS
    parse: List[Dependencies]
    tree_height: List[int]
