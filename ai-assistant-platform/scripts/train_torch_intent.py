import argparse
from pathlib import Path

import pandas as pd
import torch
from torch import nn
from torch.utils.data import DataLoader

from ai_assistant_platform.ml.dataset import IntentDataset
from ai_assistant_platform.ml.intent_model import IntentClassifier
from ai_assistant_platform.ml.label_mapping import LabelMapping
from ai_assistant_platform.ml.preprocessing import IntentPreprocessor
from ai_assistant_platform.ml.training import train_one_epoch


def main():
    # --- THÊM PHẦN NÀY ---
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", type=int, default=1, help="Số epoch cần huấn luyện")
    parser.add_argument("--batch-size", type=int, default=32, help="Kích thước batch")
    parser.add_argument("--lr", type=float, default=0.001, help="Learning rate")
    args = parser.parse_args()
    # ---------------------

    TRAIN_DATA_PATH = Path("data/splits/train.csv")
    df_train = pd.read_csv(TRAIN_DATA_PATH)

    # Trích xuất numeric & one-hot features
    preprocessor = IntentPreprocessor()
    X_train = preprocessor.fit_transform(
        df_train
    )  # Trả về ma trận numpy (N, n_features)

    # Mã hóa chuỗi text intent thành số nguyên (0, 1, 2, ...)
    label_mapping = LabelMapping()
    label_mapping.fit(df_train["intent"])
    y_train = label_mapping.encode(df_train["intent"])

    train_dataset = IntentDataset(X_train, y_train)
    train_loader = DataLoader(
        train_dataset,
        batch_size=args.batch_size,
        shuffle=True,  # Phải shuffle khi train
    )

    input_dim = X_train.shape[1]
    num_classes = len(label_mapping.classes_)

    model = IntentClassifier(
        input_dim=input_dim, hidden_dim=64, num_classes=num_classes
    )

    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr)

    for epoch in range(1, args.epochs + 1):
        avg_loss = train_one_epoch(
            model=model,
            dataloader=train_loader,
            criterion=criterion,
            optimizer=optimizer,
            device="cpu",
        )
        print(f"Epoch {epoch}/{args.epochs} - Loss: {avg_loss:.4f}")


if __name__ == "__main__":
    main()
