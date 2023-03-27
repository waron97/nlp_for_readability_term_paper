from .entry import Entry
from nltk.tokenize import sent_tokenize, word_tokenize


class Metric:
    name: str = "Metric"
    require_pos: bool = False

    def compute(self, entry: Entry) -> float:
        raise NotImplementedError


class AvgSentenceLength(Metric):
    name = "Average Sentence Length"
    require_pos = True

    def compute(self, entry: Entry) -> float:
        sents = sent_tokenize(entry["text"], language="english")
        sent_lengths = [len(word_tokenize(sent, language="english"))
                        for sent in sents]
        return sum(sent_lengths) / len(sent_lengths)


class NounToVerbRatio(Metric):
    name = "Noun to Verb Ratio"
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
    require_pos = False

    def compute(self, entry: Entry) -> float:
        tokens = word_tokenize(entry["text"], language="english")
        types = set(tokens)
        return len(types) / len(tokens)
