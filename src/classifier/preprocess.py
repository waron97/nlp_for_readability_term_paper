import re
from typing import Dict
from nltk.tokenize import word_tokenize, sent_tokenize


def clean_str(string):
    # remove punctuation
    string = re.sub(r"[^A-Za-z]", " ", string)
    # remove extra spaces
    string = re.sub(r"\s{2,}", " ", string)
    return string.strip().lower()


def encode_text(
    string,
    word2idx: Dict[str, int],
    unk_idx: int,
    limit_sents: int = None
):
    sents = sent_tokenize(string, language="english")
    if limit_sents:
        sents = sents[:limit_sents]
    sents = ".".join(sents)
    text = clean_str(sents)
    toks = word_tokenize(text, language="english")
    tok_idx = [word2idx.get(tok, unk_idx) for tok in toks]
    return tok_idx
