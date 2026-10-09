from typing import Any

import torch

from ai_assistant_platform.ml.metrics import calculate_classification_metrics


def train_one_epoch(model, dataloader, criterion, optimizer, device="cpu") -> float:
    model.train()
    total_loss = 0.0
    for feature, label in dataloader:
        feature = feature.to(device)
        label = label.to(device)
        optimizer.zero_grad()
        outputs = model(feature)
        loss = criterion(outputs, label)
        if torch.isnan(loss):
            raise RuntimeError("NaN Loss")
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    return total_loss / len(dataloader)


def evaluate_model(
    model, dataloader, criterion, device="cpu", labels=None
) -> tuple[float, dict[str, Any]]:
    model.eval()
    total_loss = 0.0
    all_preds = []
    all_targets = []

    with torch.no_grad():
        for features, targets in dataloader:
            features = features.to(device)
            targets = targets.to(device)
            outputs = model(features)
            loss = criterion(outputs, targets)
            total_loss += loss.item()

            preds = torch.argmax(outputs, dim=1)
            all_preds.extend(preds.cpu().numpy().tolist())
            all_targets.extend(targets.cpu().numpy().tolist())

    avg_loss = total_loss / len(dataloader)
    metrics = calculate_classification_metrics(all_targets, all_preds, labels=labels)
    return avg_loss, metrics
