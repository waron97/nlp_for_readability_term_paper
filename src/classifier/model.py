from torch import nn
import torch
from typing import Dict
import numpy as np
from .params_setup import get_embedding_weights


class Classifier(nn.Module):
    def __init__(
        self,
        hidden_size: int = 256,
        glove_embs: np.ndarray = None,
        word2idx: Dict[str, int] = None,
        idx2word: Dict[int, str] = None,
        load_emb_weight: bool = True
    ) -> None:
        super().__init__()
        self.glove_embs = glove_embs
        self.word2idx = word2idx
        self.idx2word = idx2word

        self.emb_size = 50
        self.embedding = nn.Embedding(len(idx2word), self.emb_size)
        if load_emb_weight:
            self._load_embedding_weight()

        self.lstm = nn.LSTM(
            input_size=self.emb_size,
            hidden_size=hidden_size,
            num_layers=3,
            batch_first=True,
        )

        self.dropout = nn.Dropout(0.1)
        self.hidden_to_output = nn.Linear(hidden_size, 2)
        self.softmax = nn.LogSoftmax(dim=1)

    def _load_embedding_weight(self):
        weight = get_embedding_weights(
            self.glove_embs, self.idx2word, self.word2idx)
        self.embedding.load_state_dict({"weight": weight})
        self.embedding.weight.requires_grad = True

    def forward(self, document_batch: torch.Tensor):
        document_batch = self.embedding(document_batch)
        # print("document_batch")
        # print(document_batch[0][0])
        # print(document_batch[1][0])
        lstm_out, _ = self.lstm(document_batch)
        lstm_out = lstm_out[:, -1, :]
        # print("lstm_out")
        # print(lstm_out[0])
        # print(lstm_out[1])
        lstm_out = self.dropout(lstm_out)
        out = self.hidden_to_output(lstm_out)
        out = self.softmax(out)
        return out
