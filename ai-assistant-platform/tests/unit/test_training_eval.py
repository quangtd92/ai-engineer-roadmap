import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

from ai_assistant_platform.ml.training import evaluate_model


def test_evaluate_model_runs_and_returns_valid_metrics():
    # 1. Tạo dummy dataset gồm 10 mẫu, mỗi mẫu 4 đặc trưng, 3 nhãn (0, 1, 2)
    dummy_x = torch.randn(10, 4, dtype=torch.float32)
    dummy_y = torch.randint(0, 3, (10,), dtype=torch.long)
    dataset = TensorDataset(dummy_x, dummy_y)
    dataloader = DataLoader(dataset, batch_size=2)

    # 2. Tạo dummy model và loss criterion
    model = nn.Linear(4, 3)
    criterion = nn.CrossEntropyLoss()

    # 3. Thực thi evaluate_model
    avg_loss, metrics = evaluate_model(
        model=model,
        dataloader=dataloader,
        criterion=criterion,
        device="cpu",
        labels=[0, 1, 2],
    )

    # 4. Kiểm tra các điều kiện assertion
    assert isinstance(avg_loss, float)
    assert avg_loss > 0.0
    assert not torch.isnan(torch.tensor(avg_loss))

    assert isinstance(metrics, dict)
    assert "macro_f1" in metrics
    assert "weighted_f1" in metrics
    assert 0.0 <= metrics["macro_f1"] <= 1.0
    assert 0.0 <= metrics["weighted_f1"] <= 1.0

    # Đảm bảo sau khi evaluate, model ở trạng thái eval
    assert model.training is False


def test_evaluate_model_does_not_modify_weights_or_compute_grad():
    dummy_x = torch.randn(6, 4, dtype=torch.float32)
    dummy_y = torch.randint(0, 3, (6,), dtype=torch.long)
    dataset = TensorDataset(dummy_x, dummy_y)
    dataloader = DataLoader(dataset, batch_size=2)

    model = nn.Linear(4, 3)
    initial_weight = model.weight.clone()
    criterion = nn.CrossEntropyLoss()

    evaluate_model(
        model=model,
        dataloader=dataloader,
        criterion=criterion,
        device="cpu",
        labels=[0, 1, 2],
    )

    # Đảm bảo trọng số không bị cập nhật
    assert torch.equal(model.weight, initial_weight)
    # Đảm bảo gradient không được tính (torch.no_grad)
    assert model.weight.grad is None
