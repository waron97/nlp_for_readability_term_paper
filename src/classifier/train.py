from .model import Classifier
from torch import nn
import torch
from torch.utils.data import DataLoader
from tqdm import tqdm
import numpy as np
from .util import de_pad


def train(
    model: Classifier,
    train_loader: DataLoader,
    optimizer: torch.optim.Optimizer,
    criterion: nn.Module,
    epochs: int = 10,
    pad_idx: int = 0
):
    model.train()
    for epoch in range(epochs):
        print(f"Epoch {epoch + 1} of {epochs}")
        pbar = tqdm(train_loader)
        for (document_batch, level_batch) in pbar:
            total_losses = 0
            for document, level in zip(document_batch, level_batch):
                optimizer.zero_grad()
                document = de_pad(document, pad_idx).unsqueeze(0)
                out = model(document)
                loss = criterion(out, level.reshape(-1))
                loss.backward()
                optimizer.step()
                total_losses += loss.item()
            total_losses = total_losses / len(document_batch)
            pbar.set_description(f"Loss: {total_losses}")

            # optimizer.zero_grad()
            # out = model(document_batch)
            # # combine losses
            # loss = criterion(out, level_batch.reshape(-1))

            # pbar.set_description(f"Loss: {loss.item()}")
            # loss.backward()

            # optimizer.step()
