import json
import os
from typing import List

from ..type import TestSet
from ..util import dump_pickle, dump_to_file, load_pickle, parse_dependencies
from .experiment import Dataset, Experiment
from .metrics import (AvgSentenceLength, ClausesPerSentence,
                      LengthLongestDependencyLink, Metric, NounToVerbRatio,
                      ParseTreeDepth, TypeTokenRatio, WordsInTop3000)


def _make_dataset(testset: TestSet) -> Dataset:
    dataset = Dataset()
    for entry in testset["gpt_generation"]:
        _id = f"{entry['level']}-{entry['topic']}"
        dataset.add_sent(_id, entry["text"], entry["level"], entry["topic"])
    for entry in testset["wikipedia"]["simple"]:
        _id = f"wikisimple-{entry['topic']}"
        dataset.add_sent(_id, entry["text"], "wikisimple", entry["topic"])
    for entry in testset["wikipedia"]["standard"]:
        _id = f"wikistandard-{entry['topic']}"
        dataset.add_sent(_id, entry["text"], "wikistandard", entry["topic"])
    return dataset


def _make_metrics() -> List[Metric]:
    return [
        AvgSentenceLength(),
        NounToVerbRatio(),
        TypeTokenRatio(),
        ClausesPerSentence(),
        LengthLongestDependencyLink(),
        ParseTreeDepth(),
        WordsInTop3000()
    ]


def analyze_dataset():
    with open("data/dataset/dataset.json", "r", encoding="utf-8") as f:
        testset: TestSet = json.load(f)

    dataset = _make_dataset(testset)
    metrics = _make_metrics()
    experiment: Experiment = None
    pickle_path = "data/experiment_data.pickle"

    if os.path.exists(pickle_path):
        empty_dataset = Dataset()
        experiment = Experiment(empty_dataset, metrics, preprocess=False)
        experiment.load_dataset_from_pkl(pickle_path)
    else:
        experiment = Experiment(dataset, metrics)
        experiment.dump_dataset_to_pkl(pickle_path)

    experiment.compute_metrics()
    dump_to_file(experiment.results.all(), "data/results.json")

    return metrics, experiment
