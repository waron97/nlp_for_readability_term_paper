import torch
from torch import nn
from torch.optim import Adam
from torch.utils.data import DataLoader
import os

from .model import Classifier
from .params_setup import build_vocabulary
from .load_data import get_train_test_ids, load_glove_data
from .dataset import WikiArticleDataset
from .device import device
from .train import train
from .evaluate import evaluate


def train_classifier():
    print("Getting ids")
    train_ids, test_ids = get_train_test_ids(train_limit=1000)
    print("Loading glove data")
    glove_word2idx, glove_idx2word, glove_embs = load_glove_data()
    print("Building vocabulary")
    vocab_word2idx, vocab_idx2word, unk_idx, pad_idx, max_tokens = build_vocabulary(
        train_ids, glove_word2idx, glove_idx2word)
    print(f"Longest entry has {max_tokens} tokens")
    print("Loading datasets")
    train_dataset = WikiArticleDataset(
        train_ids,
        vocab_word2idx,
        unk_idx, pad_idx,
        pad_to_size=max_tokens,
    )
    test_dataset = WikiArticleDataset(
        test_ids,
        vocab_word2idx,
        unk_idx, pad_idx,
        pad_to_size=max_tokens,
    )
    train_dataloader = DataLoader(train_dataset, batch_size=64, shuffle=True)
    test_dataloader = DataLoader(test_dataset, batch_size=64, shuffle=True)

    model_path = "data/classifier_data/model.pt"

    print("Loading model")
    if os.path.exists(model_path):
        model = Classifier(
            glove_embs=glove_embs,
            word2idx=vocab_word2idx,
            idx2word=vocab_idx2word,
            load_emb_weight=False
        )
        print("Loading model weights")
        model.load_state_dict(torch.load(model_path))
        print("Model loaded, moving to device")
        model.to(device)

    else:
        model = Classifier(
            glove_embs=glove_embs,
            word2idx=vocab_word2idx,
            idx2word=vocab_idx2word,
            load_emb_weight=True
        )
        model.to(device)
        optimizer = Adam(model.parameters(), lr=0.005)
        criterion = nn.NLLLoss()
        train(model, train_dataloader, optimizer,
              criterion, epochs=5, pad_idx=pad_idx)
        torch.save(model.state_dict(), model_path)

    print("Evaluating model")
    evaluate(model, test_dataloader)
