from typing import Dict, List
from sqlalchemy.orm import Session
from src.sql.models import WikiArticle
from src.sql import engine
import numpy as np


def load_glove_data():
    p = "data/glove.6B/glove.6B.50d.txt"
    word2idx: Dict[str, int] = {}
    idx2word: Dict[int, str] = {}
    embs: List[List[float]] = []
    with open(p, "r", encoding="utf-8") as file:
        i = 0
        for l in file:
            l = l.split()
            word, emb = l[0], l[1:]
            emb = [float(x) for x in emb]
            word2idx[word] = i
            idx2word[i] = word
            embs.append(emb)
            i += 1

    return word2idx, idx2word, np.array(embs)


def get_train_test_ids(test_portion_size: float = 0.1):
    with Session(engine) as session:
        _ids = []
        items = session.query(WikiArticle.id).limit(10_000).all()
        for item in items:
            _id = item[0]
            _ids.append((_id, "standard"))
            _ids.append((_id, "simple"))
    train_size = 1 - test_portion_size
    train = _ids[:int(len(_ids) * train_size)]
    test = _ids[int(len(_ids) * train_size):]
    return train, test
