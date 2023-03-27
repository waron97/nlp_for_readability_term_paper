from typing import List

from ..experiment.metrics import Metric
from ..experiment.experiment import Experiment
from matplotlib import pyplot as plt
from ..constants import TOPICS, LEVELS
import pandas as pd


def _map_metric_name(name):
    if name == "wikisimple":
        return "S Wiki"
    elif name == "wikistandard":
        return "Wiki"
    return name


def _make_table(metrics: List[Metric], experiment: Experiment):
    columns = [metric.abbreviation for metric in metrics]
    index = LEVELS + ["wikisimple", "wikistandard"]
    index_mapped = list(map(_map_metric_name, index))

    df = pd.DataFrame(index=index_mapped, columns=columns)
    for metric in metrics:
        for level in index:
            try:
                value = experiment.results.filter(
                    metrics=[metric.name], levels=[level]).mean(metric.name)
                value = round(value, 3)
                df.loc[_map_metric_name(level), metric.abbreviation] = value
            except ZeroDivisionError:
                print(
                    f"ZeroDivisionError for {metric.abbreviation} and {level}! Skipping...")
    print(df.to_latex())


def _make_topic_metric_plot(metric: str, topic: str, experiment: Experiment, short_name: str = ""):
    values = experiment.results.filter(
        metrics=[metric], idlike=topic).all()

    levels = [_map_metric_name(value["level"]) for value in values]
    tups = [(level, value["value"]) for level, value in zip(levels, values)]
    tups.sort(key=lambda tup: tup[1])

    x = list(range(len(tups)))
    height = [tup[1] for tup in tups]
    labels = [tup[0] for tup in tups]
    plt.bar(x, height, tick_label=labels, width=0.8,)
    plt.xticks(rotation=45)
    fname = f"plot_{short_name}_{topic}.png" if short_name else f"plot_{metric}_{topic}.png"
    plt.savefig(f"data/analysis/topics/{fname}")
    plt.cla()


def _make_plot(metric: str, experiment: Experiment, short_name: str = "", sort_revert: bool = False):
    a1 = experiment.results.filter(
        metrics=[metric], levels=["A1"]).mean(metric)
    a2 = experiment.results.filter(
        metrics=[metric], levels=["A2"]).mean(metric)
    b1 = experiment.results.filter(
        metrics=[metric], levels=["B1"]).mean(metric)
    b2 = experiment.results.filter(
        metrics=[metric], levels=["B2"]).mean(metric)
    c1 = experiment.results.filter(
        metrics=[metric], levels=["C1"]).mean(metric)
    c2 = experiment.results.filter(
        metrics=[metric], levels=["C2"]).mean(metric)
    simple = experiment.results.filter(
        metrics=[metric], levels=["wikisimple"]).mean(metric)
    standard = experiment.results.filter(
        metrics=[metric], levels=["wikistandard"]).mean(metric)

    tups = [
        ("A1", a1),
        ("A2", a2),
        ("B1", b1),
        ("B2", b2),
        ("C1", c1),
        ("C2", c2),
        ("S Wiki", simple),
        ("Wiki", standard)
    ]
    tups.sort(key=lambda tup: tup[1], reverse=sort_revert)

    x = list(range(len(tups)))
    height = [tup[1] for tup in tups]
    tick_label = [tup[0] for tup in tups]

    plt.bar(x, height, tick_label=tick_label, width=0.8, label=metric)
    fname = f"plot_{short_name}.png" if short_name else f"plot_{metric}.png"
    plt.savefig(f"data/analysis/metric_means/{fname}")
    plt.cla()
    # plt.show()


def plot_results(metrics: List[Metric], experiment: Experiment):
    # for metric in metrics:
    #     for topic in TOPICS:
    #         _make_topic_metric_plot(
    #             metric.name, topic, experiment, short_name=metric.abbreviation)
    _make_plot("Words in Top 3000", experiment,
               short_name="WIT", sort_revert=True)

    # for metric in metrics:
    #     _make_plot(metric.name, experiment, short_name=metric.abbreviation)

    _make_table(metrics, experiment)
