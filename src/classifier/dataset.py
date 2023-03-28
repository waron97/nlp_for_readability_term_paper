from typing import Dict, List, Tuple
from torch.utils.data import Dataset

from sqlalchemy.orm import Session
from src.sql.models import ClassifierDataset
from src.sql import engine
from .preprocess import encode_text

from .device import device
import torch


class WikiArticleDataset(Dataset):
    def __init__(
        self, ids: List[Tuple[int, str]],
        word2idx: Dict[str, int],
        unk_tok_idx: int,
        pad_token_idx: int,
        pad_to_size: int = 1000,
        sent_limit: int = None
    ) -> None:
        super().__init__()
        self._ids = ids
        self.word2idx = word2idx
        self.unk_idx = unk_tok_idx
        self.pad_size = pad_to_size
        self.pad_idx = pad_token_idx
        self.sent_limit = sent_limit

    def __len__(self):
        return len(self._ids)

    def __getitem__(self, index) -> Tuple[str, str]:
        _id, level = self._ids[index]
        with Session(engine) as session:
            item = session.query(ClassifierDataset).filter_by(id=_id).first()
            text = item.text
        tok_idx = encode_text(
            text,
            self.word2idx,
            self.unk_idx,
            limit_sents=self.sent_limit
        )
        tok_idx = torch.tensor(tok_idx, device=device, dtype=torch.long)

        if len(tok_idx) < self.pad_size:
            pad = torch.tensor(
                [self.pad_idx] * (self.pad_size - len(tok_idx)), device=device, dtype=torch.long)
            tok_idx = torch.cat([tok_idx, pad])
        elif len(tok_idx) > self.pad_size:
            tok_idx = tok_idx[:self.pad_size]

        level = torch.tensor(
            [1], device=device) if level == "standard" else torch.tensor([0], device=device)
        return tok_idx, level
