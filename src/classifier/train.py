from .model import Classifier
from torch import nn
import torch
from torch.utils.data import DataLoader
from tqdm import tqdm
import numpy as np


def train(
    model: Classifier,
    train_loader: DataLoader,
    optimizer: torch.optim.Optimizer,
    criterion: nn.Module,
    epochs: int = 10,
):
    model.train()
    for epoch in range(epochs):
        print(f"Epoch {epoch + 1} of {epochs}")
        pbar = tqdm(train_loader)
        for (document_batch, level_batch) in pbar:
            optimizer.zero_grad()
            out = model(document_batch)
            # combine losses
            loss = criterion(out, level_batch.reshape(-1))

            pbar.set_description(f"Loss: {loss.item()}")
            loss.backward()

            optimizer.step()
