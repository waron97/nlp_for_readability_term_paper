
from src.simple_wiki import load_simple_wiki_sql, load_full_wikipedia_dataset_sql
from dotenv import load_dotenv
from src.make_dataset import make_dataset, write_dataset
from src.experiment import analyze_dataset, plot_results

load_dotenv()


def main():
    load_full_wikipedia_dataset_sql()
    # load_simple_wiki_sql()
    # make_dataset()
    # write_dataset()
    metrics, experiment = analyze_dataset()
    plot_results(metrics, experiment)


if __name__ == "__main__":
    main()
