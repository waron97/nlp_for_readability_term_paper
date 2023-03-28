import pickle
import os
from typing import Dict, List, Tuple
from tqdm import tqdm
import numpy as np
import torch

from .util import random_vector
from .device import device
from sqlalchemy.orm import Session
from src.sql.models import ClassifierDataset
from src.sql import engine
from .preprocess import clean_str
from nltk.tokenize import word_tokenize


def build_vocabulary(train_ids: List[Tuple[int, str]], glove_word2idx: Dict[str, int],  glove_idx2word: Dict[int, str]):
    pickle_path = "data/classifier_data/vocabulary.pkl"

    if os.path.exists(pickle_path):
        with open(pickle_path, "rb") as file:
            payload = pickle.load(file)
            return payload["word2idx"], payload["idx2word"], payload["unk_idx"], payload["pad_idx"], payload["max_tokens"]

    word2idx: Dict[str, int] = {}
    idx2word = {}

    for idx, word in glove_idx2word.items():
        word2idx[word] = idx
        idx2word[idx] = word

    voc = set()
    max_tokens = 0
    with Session(engine) as session:
        for _id, level in tqdm(train_ids):
            doc = session.query(ClassifierDataset).filter_by(id=_id).first()
            text = doc.text
            text = clean_str(text)
            tokens = word_tokenize(text)
            for token in tokens:
                voc.add(token)
            max_tokens = max(max_tokens, len(tokens))

    # unprocessed = []
    # for word in voc:
    #     glove_idx = glove_word2idx.get(word)
    #     if glove_idx is None:
    #         unprocessed.append(word)

    # i = len(word2idx)
    # for word in unprocessed:
    #     while idx2word.get(i) is not None:
    #         i += 1
    #     word2idx[word] = i
    #     idx2word[i] = word
    #     i += 1

    unk_idx = len(word2idx)
    while idx2word.get(unk_idx) is not None:
        unk_idx += 1
    unk = "<UNK>"
    word2idx[unk] = unk_idx
    idx2word[unk_idx] = unk

    pad_idx = len(word2idx)
    while idx2word.get(pad_idx) is not None:
        pad_idx += 1
    pad = "<PAD>"
    word2idx[pad] = pad_idx
    idx2word[pad_idx] = pad

    pickle_payload = {
        "word2idx": word2idx,
        "idx2word": idx2word,
        "unk_idx": unk_idx,
        "pad_idx": pad_idx,
        "max_tokens": max_tokens
    }

    with open(pickle_path, "wb") as file:
        pickle.dump(pickle_payload, file)

    return word2idx, idx2word, unk_idx, pad_idx, max_tokens


def get_embedding_weights(embs: np.ndarray, idx2word: Dict[int, str]):
    embedding_dim = 50
    vocab_size = len(idx2word)
    weight_matrix = torch.zeros((vocab_size, embedding_dim))
    for idx in idx2word:
        if idx < len(embs):
            weight_matrix[idx] = torch.tensor(
                embs[idx], device=device, dtype=torch.float32)
        else:
            weight_matrix[idx] = random_vector(embedding_dim)
    return weight_matrix
