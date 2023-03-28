import torch
from .device import device


def random_vector(size: int) -> torch.Tensor:
    return torch.rand(size, device=device, dtype=torch.float32)


def de_pad(tensor: torch.Tensor, pad_idx: int):
    t_new = []
    for t in tensor:
        if t.item() == pad_idx:
            break
        else:
            t_new.append(t.item())
    return torch.tensor(t_new, device=device, dtype=torch.long)
