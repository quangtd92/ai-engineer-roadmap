# Gợi ý khung test cho tests/unit/test_training_step.py
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

from ai_assistant_platform.ml.training import train_one_epoch


def test_train_one_epoch_runs_successfully():
    # 1. Tạo dummy features và labels
    # 10 samples, mỗi sample 4 features
    dummy_x = torch.randn(10, 4, dtype=torch.float32)
    dummy_y = torch.randint(0, 3, (10,), dtype=torch.long)
    print(f"Dummy X: {dummy_x}, Dummy Y: {dummy_y}")
    dataset = TensorDataset(dummy_x, dummy_y)
    dataloader = DataLoader(dataset, batch_size=2)

    # 2. Tạo model tuyến tính đơn giản làm dummy model
    model = nn.Linear(4, 3)
    print(f"model: {model}")
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

    # 3. Gọi hàm train
    loss = train_one_epoch(model, dataloader, criterion, optimizer, device="cpu")

    # 4. Kiểm tra điều kiện (Assertions)
    assert isinstance(loss, float)
    assert loss > 0.0
    assert not torch.isnan(torch.tensor(loss))
