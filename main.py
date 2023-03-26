
from src.clear_corpus import create_corpus_table
from dotenv import load_dotenv
from src.make_dataset import make_dataset

load_dotenv()


def main():
    make_dataset()


if __name__ == "__main__":
    main()
