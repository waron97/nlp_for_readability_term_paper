from .model import Classifier
from torch import nn
import torch
from torch.utils.data import DataLoader
from tqdm import tqdm


def train(
    model: Classifier,
    train_loader: DataLoader,
    optimizer: torch.optim.Optimizer,
    criterion: nn.Module,
    epochs: int = 10,
):
    for epoch in range(epochs):
        print(f"Epoch {epoch + 1} of {epochs}")
        pbar = tqdm(train_loader)
        for (document_batch, level_batch) in pbar:
            optimizer.zero_grad()
            out = model(document_batch)
            # combine losses
            loss = 0
            for i in range(out.shape[0]):
                prediction = out[i].unsqueeze(0)
                correct = level_batch[i]
                loss += criterion(prediction, correct)
            pbar.set_description(f"Loss: {loss.item()}")
            loss.backward()

            optimizer.step()
