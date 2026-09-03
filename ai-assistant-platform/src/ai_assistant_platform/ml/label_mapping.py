from collections.abc import Iterable

import numpy as np
from sklearn.preprocessing import LabelEncoder


class LabelMapping:
    def __init__(self):
        self.label_encoder = LabelEncoder()
        self.is_fit = False
        self.classes_: list[str] = []

    def fit(self, labels: Iterable[str]) -> "LabelMapping":
        unique_labels  = sorted(set(labels))
        self.label_encoder.fit(unique_labels)
        self.is_fit = True
        self.classes_ = list(self.label_encoder.classes_)

        return self

    def transform(self, label: Iterable[str]) -> np.ndarray:
        if not self.is_fit:
            raise ValueError("You must fit the label mapping before transforming data")
        return self.label_encoder.transform(label)

    def inverse_transform(self, indices: Iterable[int]) -> np.ndarray:
        if not self.is_fit:
            raise ValueError("You must fit the label mapping before transforming data")
        return self.label_encoder.inverse_transform(indices)
    
    def encode(self, labels: Iterable[str]) -> list[int]:
        return self.transform(labels)
    
    def decode(self, indices: Iterable[int]) -> list[str]:
        return self.inverse_transform(indices)
