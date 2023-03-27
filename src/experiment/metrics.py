from string import punctuation
from .entry import Entry
from nltk.tokenize import sent_tokenize, word_tokenize
import csv


class Metric:
    name: str = "Metric"
    abbreviation: str = "met"
    require_pos: bool = False

    def compute(self, entry: Entry) -> float:
        raise NotImplementedError


class AvgSentenceLength(Metric):
    name = "Average Sentence Length"
    abbreviation = "ASL"
    require_pos = True

    def compute(self, entry: Entry) -> float:
        sents = sent_tokenize(entry["text"], language="english")
        sent_lengths = [len(word_tokenize(sent, language="english"))
                        for sent in sents]
        return sum(sent_lengths) / len(sent_lengths)


class NounToVerbRatio(Metric):
    name = "Noun to Verb Ratio"
    abbreviation = "NVR"
    require_pos = True

    def compute(self, entry: Entry) -> float:
        nouns = 0
        verbs = 0
        noun_tags = ["NOUN", "PROPN"]
        verb_tags = ["VERB"]
        for sent in entry["pos"]:
            for token, tag in sent:
                if tag in noun_tags:
                    nouns += 1
                elif tag in verb_tags:
                    verbs += 1
        try:
            return nouns / verbs
        except ZeroDivisionError:
            return 0.0


class TypeTokenRatio(Metric):
    name = "Type Token Ratio"
    abbreviation = "TTR"
    require_pos = False

    def compute(self, entry: Entry) -> float:
        tokens = word_tokenize(entry["text"], language="english")[:100]
        types = set(tokens)
        return len(types) / len(tokens)


class ClausesPerSentence(Metric):
    name = "Clauses Per Sentence"
    abbreviation = "CPS"

    def compute(self, entry: Entry) -> float:
        sentence_relations = entry["parse"]
        clause_relations = ["root", "ccomp",
                            "xcomp", "advcl", "acl", "acl:relcl"]

        n_clauses = 0
        for sent in sentence_relations:
            for row in sent.rows:
                if row["rel"].lower() in clause_relations:
                    n_clauses += 1

        return n_clauses / len(sentence_relations)


class LengthLongestDependencyLink(Metric):
    name = "Length of Longest Dependency Link"
    abbreviation = "LLDL"

    def compute(self, entry: Entry) -> float:
        sentence_relations = entry["parse"]
        exclude = ["punct"]
        values = []
        for sent in sentence_relations:
            longest = 0
            for row in sent.rows:
                idx = int(row["id"])
                head = int(row["head"])
                distance = abs(idx - head)
                if distance > longest and row["rel"] not in exclude:
                    longest = distance
            values.append(longest)
        return sum(values) / len(sentence_relations)


class ParseTreeDepth(Metric):
    name = "Parse Tree Depth"
    abbreviation = "PTD"

    def compute(self, entry: Entry) -> float:
        values = entry["tree_height"]
        return sum(values) / len(values)


class WordsInTop3000(Metric):
    name = "Words in Top 3000"
    abbreviation = "WIT"

    def __init__(self) -> None:
        p = "data/unigram_freq.csv"
        self.top_3000 = set()
        with open(p, "r") as f:
            reader = csv.reader(f, delimiter=",")
            next(reader)  # skip header
            for _ in range(3000):
                row = next(reader)
                self.top_3000.add(row[0])

    def compute(self, entry: Entry) -> float:
        tokens = word_tokenize(entry["text"], language="english")
        tokens = [token.lower() for token in tokens if token not in [
            ",", ".", "?", "!", ":", ";"]]

        in_top_3000 = 0
        for token in tokens:
            if token in self.top_3000:
                in_top_3000 += 1

        return in_top_3000 / len(tokens)
