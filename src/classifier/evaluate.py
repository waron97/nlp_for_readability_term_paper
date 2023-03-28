from sklearn.metrics import precision_recall_fscore_support
from torch.utils.data import DataLoader
from .model import Classifier


def evaluate(model: Classifier, test_dataloader: DataLoader):
    y_true = []
    y_pred = []
    for document_batch, level_batch in test_dataloader:
        out = model(document_batch)
        y_true.extend(level_batch.reshape(-1).tolist())
        out = out.argmax(dim=1).reshape(-1).tolist()
        y_pred.extend(out)
    precision, recall, fscore, support = precision_recall_fscore_support(
        y_true, y_pred, average="macro")
    print(f"Precision:\t{precision}\nRecall:\t{recall}\nF1\t{fscore}")
