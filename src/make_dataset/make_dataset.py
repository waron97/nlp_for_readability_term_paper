

from ..gpt import GPT3
from ..sql.engine import engine
from ..sql.models import DatasetEntry
from sqlalchemy.orm import Session
from typing import List, Tuple
from tqdm import tqdm


TOPICS = ["Computational Linguistics"]
LEVELS = ["C2"]


def _create_prompts() -> List[Tuple[str, str, str]]:
    prompts = []
    for level in LEVELS:
        for topic in TOPICS:
            prompt = f"Write a text for learners of English at the {level} level about {topic}."
            prompts.append((prompt, level, topic))
    return prompts


def _exists(level, topic):
    with Session(engine) as session:
        entry = session.query(DatasetEntry).filter_by(
            level=level, topic=topic).first()
        return entry is not None


def _save_generation(text, level, topic, prompt):
    with Session(engine) as session:
        entry = DatasetEntry(model="GPT-3", level=level,
                             topic=topic, text=text, prompt=prompt)
        session.add(entry)
        session.commit()


def make_dataset():
    prompts = _create_prompts()
    gpt3 = GPT3()
    for prompt, level, topic in tqdm(prompts):
        if _exists(level, topic):
            continue
        text = gpt3.complete(prompt)
        _save_generation(text, level, topic, prompt)
