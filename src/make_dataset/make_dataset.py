from pprint import pprint

from ..gpt import GPT3
from ..util import dump_to_file


TOPICS = ["Computational Linguistics"]
LEVELS = ["C2"]


def _create_prompts():
    prompts = []
    for level in LEVELS:
        for topic in TOPICS:
            prompt = f"Write a text for learners of English at the {level} level about {topic}."
            prompts.append(prompt)
    return prompts


def make_dataset():
    prompts = _create_prompts()
    gpt3 = GPT3()
    completion = gpt3.complete(prompt=prompts[0])
    dump_to_file(completion, "completion.txt", json=False)
