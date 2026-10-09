import numpy as np
import torch

from ai_assistant_platform.ml.dataset import IntentDataset


def test_intent_dataset():
    # X có 3 dòng (3 mẫu), 4 cột (4 features)
    X = np.array(
        [
            [0.10, 0.50, 0.00, 0.20],  # Mẫu index 0
            [0.00, 0.80, 0.30, 0.10],  # Mẫu index 1
            [0.90, 0.00, 0.10, 0.40],  # Mẫu index 2
        ]
    )
    # y chứa nhãn của 3 mẫu
    y = np.array([0, 1, 0])

    dataset = IntentDataset(X, y)

    assert len(dataset) == 3
    # 1. Log độ dài dataset
    print(f"\n[LOG] Len dataset: {len(dataset)}")
    # 2. Log mẫu đầu tiên
    features, label = dataset[0]
    print(f"[LOG] Features sample 0: {features}")
    print(f"[LOG] Features shape: {features.shape}, dtype: {features.dtype}")
    print(f"[LOG] Label sample 0: {label}")
    print(f"[LOG] Label shape: {label.shape}, dtype: {label.dtype}")

    assert features.dtype == torch.float32
    assert label.dtype == torch.long
