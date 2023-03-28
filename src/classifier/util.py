import torch
from .device import device


def random_vector(size: int) -> torch.Tensor:
    return torch.rand(size, device=device, dtype=torch.float32)
