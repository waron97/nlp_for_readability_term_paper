import torch

if torch.backends.mps.is_available() and torch.backends.mps.is_built():
    device = torch.device("cpu")
else:
    device = torch.device("cpu")
