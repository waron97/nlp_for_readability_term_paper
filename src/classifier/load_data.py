from typing import Dict, List
from sqlalchemy.orm import Session
from src.sql.models import ClassifierDataset
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


def get_train_test_ids(train_limit: int = 200_000, test_limit: int = 20_000):
    train, test = [], []
    with Session(engine) as session:
        q_simple_train = session.query(ClassifierDataset).filter_by(
            level="simple", partition="train").limit(train_limit)
        q_standard_train = session.query(ClassifierDataset).filter_by(
            level="standard", partition="train").limit(train_limit)
        q_simple_test = session.query(ClassifierDataset).filter_by(
            level="simple", partition="test").limit(test_limit)
        q_standard_test = session.query(ClassifierDataset).filter_by(
            level="standard", partition="test").limit(test_limit)
        for item in q_simple_train:
            train.append((item.id, "simple"))
        for item in q_standard_train:
            train.append((item.id, "standard"))
        for item in q_simple_test:
            test.append((item.id, "simple"))
        for item in q_standard_test:
            test.append((item.id, "standard"))
    return train, test
