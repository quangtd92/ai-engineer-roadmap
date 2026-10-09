import numpy as np
import torch
from scipy.sparse import issparse
from torch.utils.data import DataLoader, Dataset


class IntentDataset(Dataset):
    def __init__(self, X: np.ndarray, y: np.ndarray):
        # Check and convert sparse matrix (if right) to dense array
        if issparse(X):
            X = X.toarray()
        elif hasattr(X, "values"):  # If X is pandas DataFrame
            X = X.values

        if hasattr(y, "values"):  # If y is pandas Series
            y = y.values

        # Convert to tensor with the correct dtype
        self.X = torch.tensor(X, dtype=torch.float32)
        self.y = torch.tensor(y, dtype=torch.long)

    def __len__(self) -> int:
        """Return the number of samples in the dataset."""
        return len(self.X)

    def __getitem__(self, idx: int) -> tuple:
        """Return the sample and label at the given index."""
        return self.X[idx], self.y[idx]


def create_intent_dataloaders(
    train_dataset: Dataset, val_dataset: Dataset, batch_size: int = 32
) -> tuple[DataLoader, DataLoader]:
    """Tạo DataLoader cho tập train (shuffle=True) và val (shuffle=False)."""
    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
    )
    val_loader = DataLoader(
        val_dataset,
        batch_size=batch_size,
        shuffle=False,
    )
    return train_loader, val_loader
