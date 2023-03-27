

import json
import requests
from ..gpt import GPT3
from ..sql.engine import engine
from ..sql.models import DatasetEntry, DatasetWikiText, SimpleWikiEntry
from sqlalchemy.orm import Session
from typing import List, Tuple
from tqdm import tqdm
from ..util import dump_to_file


TOPICS = [
    "Color Blindness",
    "The Great Depression",
    "Butterflies",
    "Dogs",
    "Semantics",
    "The Internet",
    "The Moon",
    "Dinosaurs",
    "Economics",
    "Quantum Mechanics",
]

LEVELS = [
    "A1",
    "A2",
    "B1",
    "B2",
    "C1",
    "C2"
]

WIKI_TOPICS = [
    "Color Blindness",
    "Great Depression",
    "Butterfly",
    "Dog",
    "Semantics",
    "Internet",
    "Moon",
    "Dinosaur",
    "Economics",
    "Quantum Mechanics",
]


def _get_standard_wiki_text(topic):
    content = requests.post(
        "http://localhost:6000/article",
        headers={"Content-Type": "application/json"},
        data=json.dumps({"title": topic})
    )
    l = json.loads(content.content)
    return l["text"]


def _get_simple_wiki_text(topic):
    with Session(engine) as session:
        row = session.query(SimpleWikiEntry).filter(
            SimpleWikiEntry.title.like(f"{topic}")).first()
        return row.text_clean


def _create_prompts() -> List[Tuple[str, str, str, str]]:
    prompts = []
    for level in LEVELS:
        for i, topic in enumerate(TOPICS):
            prompt = f"Write a text for learners of English at the {level} level about {topic}."
            prompts.append((prompt, level, topic, WIKI_TOPICS[i]))
    return prompts


def _exists(level, topic):
    with Session(engine) as session:
        entry = session.query(DatasetEntry).filter_by(
            level=level, topic=topic).first()
        return entry is not None


def _create_wiki_record(topic):
    with Session(engine) as session:
        if session.query(DatasetWikiText).filter_by(topic=topic).first():
            return
        standard_wiki = _get_standard_wiki_text(topic)
        simple_wiki = _get_simple_wiki_text(topic)
        entry = DatasetWikiText(topic=topic, standard=standard_wiki,
                                simple=simple_wiki)
        session.add(entry)
        session.commit()


def _save_generation(text, level, topic, prompt):
    with Session(engine) as session:
        entry = DatasetEntry(model="GPT-3", level=level,
                             topic=topic, text=text, prompt=prompt)
        session.add(entry)
        session.commit()


def make_dataset():
    prompts = _create_prompts()
    gpt3 = GPT3()
    for i, (prompt, level, topic, wiki_topic) in tqdm(enumerate(prompts)):
        _create_wiki_record(wiki_topic)
        if _exists(level, topic):
            continue
        text = gpt3.complete(prompt)
        _save_generation(text, level, topic, prompt)
