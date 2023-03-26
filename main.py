import json

from src.dalle import DALL_E
from src.gpt import GPT3
from src.clear_corpus import create_corpus_table
from dotenv import load_dotenv

from src.util.core import dump_to_file
load_dotenv()


def main():
    create_corpus_table()
    gpt3 = GPT3()
    # completion = gpt3.complete(
    #     "Write a text for learners of English at the A1 level about computational linguistics."
    # )
    # dump_to_file(json.dumps(completion, indent=2), "completion.json")


if __name__ == "__main__":
    main()
