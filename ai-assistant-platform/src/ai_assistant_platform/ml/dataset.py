import numpy as np
import torch
from scipy.sparse import issparse
from torch.utils.data import Dataset


class IntentDataset(Dataset):
    def __init__(self, X: np.ndarray, y: np.ndarray):
        # Check and convert sparse matrix (if right) to dense array
        if issparse(X):
            X = X.toarray()
        elif hasattr(X, 'values'): # If X is pandas DataFrame
            X = X.values

        if hasattr(y, 'values'): # If y is pandas Series
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