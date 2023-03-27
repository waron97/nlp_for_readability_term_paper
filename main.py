
from os import write
from tkinter import W
from src.clear_corpus import create_corpus_table
from src.simple_wiki import load_simple_wiki_sql
from dotenv import load_dotenv
from src.make_dataset import make_dataset, write_dataset

load_dotenv()


def main():
    # create_corpus_table()
    # load_simple_wiki_sql()
    make_dataset()
    write_dataset()


if __name__ == "__main__":
    main()
