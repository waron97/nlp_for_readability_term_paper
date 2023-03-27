
from src.simple_wiki import load_simple_wiki_sql
from dotenv import load_dotenv
from src.make_dataset import make_dataset, write_dataset

load_dotenv()


def main():
    load_simple_wiki_sql()
    make_dataset()
    write_dataset()


if __name__ == "__main__":
    main()
