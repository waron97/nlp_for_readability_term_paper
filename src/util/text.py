from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tag import pos_tag_sents
from typing import List, Tuple
from nltk.parse.corenlp import CoreNLPParser, CoreNLPServer, CoreNLPDependencyParser
from nltk.tree.tree import Tree
from nltk.parse.dependencygraph import DependencyGraph
import os

from ..type import Dependencies


def tokenize_text(text: str) -> List[List[str]]:
    t = text.replace("\n", " ").strip()
    sents = sent_tokenize(t, language="english")
    return [word_tokenize(sent, language="english") for sent in sents]


POS_TAGS = List[List[Tuple[str, str]]]


def pos_tag_text(text: str) -> POS_TAGS:
    t = text.replace("\n", " ").strip()
    sents = sent_tokenize(t, language="english")
    sent_tokens = [word_tokenize(sent, language="english") for sent in sents]
    return pos_tag_sents(sent_tokens, tagset="universal", lang="eng")


def _parse_graph(graph: DependencyGraph) -> Tuple[Dependencies, int]:
    tree_height = graph.tree().height()
    conll = graph.to_conll(10).strip().split("\n")
    d = Dependencies()
    for line in conll:
        spl = line.split("\t")
        idx, word, lemma, pos, tag, _, head, rel, _, _ = spl
        d.add_row(idx, word, lemma, pos, tag, head, rel)
    return d, tree_height


def parse_dependencies(text: str) -> List[Tuple[Dependencies, int]]:
    jar_path = os.path.join(
        os.getcwd(), "data", "stanford-corenlp-4.5.4", "stanford-corenlp-4.5.4.jar")
    models_path = os.path.join(
        os.getcwd(), "data", "stanford-corenlp-4.5.4", "stanford-corenlp-4.5.4-models.jar")
    with CoreNLPServer(path_to_jar=jar_path, path_to_models_jar=models_path) as server:
        parser = CoreNLPDependencyParser(url=server.url)
        sentences = sent_tokenize(text, language="english")
        sentences = parser.raw_parse_sents(sentences)
        graphs = [list(sentence)[0] for sentence in sentences]
        return [_parse_graph(graph) for graph in graphs]
