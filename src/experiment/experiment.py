from typing import List, Tuple, TypedDict

from ..util import some, pos_tag_text, parse_dependencies
from .entry import Entry
from .metrics import Metric
from ..type import Dependencies
from tqdm import tqdm
import pickle


class Dataset:
    def __init__(self) -> None:
        self.data: List[Entry] = []

    def add_sent(self, id: str, text: str):
        self.data.append({
            "id": id,
            "text": text,
            "pos": [],
            "parse": []
        })


class Result(TypedDict):
    id: str
    metric: str
    value: float


class ResultSet:
    def __init__(self, results: List[Result]) -> None:
        self.results = results

    def get(self, id: str, metric: str) -> float:
        for result in self.results:
            if result["id"] == id and result["metric"] == metric:
                return result["value"]
        raise KeyError(f"Result for {id} and {metric} not found.")

    def all(self):
        return self.results

    def filter(self, ids: List[str], metrics: List[str]) -> List[Result]:
        results: List[Result] = []
        for result in self.results:
            if result["id"] in ids or result["metric"] in metrics:
                results.append(result)
        return results


class Experiment:
    def __init__(self, dts: Dataset, metrics: List[Metric], preprocess: bool = True) -> None:
        self.dataset: Dataset = dts
        self.metrics: List[Metric] = metrics
        self.results: ResultSet = ResultSet([])
        if preprocess:
            self._tag()
            self._parse()

    def _tag(self):
        print("Tagging...")
        for i, entry in tqdm(enumerate(self.dataset.data), total=len(self.dataset.data)):
            tokens = pos_tag_text(entry["text"])
            self.dataset.data[i]["pos"] = tokens

    def _parse(self):
        print("Parsing...")
        for i, entry in tqdm(enumerate(self.dataset.data), total=len(self.dataset.data)):
            parse = parse_dependencies(entry["text"])
            self.dataset.data[i]["parse"] = parse

    def compute_metrics(self):
        results: List[Result] = []
        for metric in self.metrics:
            for entry in self.dataset.data:
                value = round(metric.compute(entry), 4)
                results.append({
                    "id": entry["id"],
                    "metric": metric.name,
                    "value": value})
        self.results = ResultSet(results)

    def load_dataset_from_pkl(self, fpath: str):
        with open(fpath, "rb") as f:
            self.dataset = pickle.load(f)

    def dump_dataset_to_pkl(self, fpath: str):
        with open(fpath, "wb") as f:
            pickle.dump(self.dataset, f)
