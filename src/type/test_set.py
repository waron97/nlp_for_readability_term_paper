from typing import Dict, List, TypedDict


class GPT_Record(TypedDict):
    topic: str
    level: str
    text: str


class Wiki_Record(TypedDict):
    topic: str
    text: str


class Wiki_Set(TypedDict):
    simple: List[Wiki_Record]
    standard: List[Wiki_Record]


class TestSet(TypedDict):
    gpt_generation: List[GPT_Record]
    wikipedia: Wiki_Set
