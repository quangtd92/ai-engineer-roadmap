import torch


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
