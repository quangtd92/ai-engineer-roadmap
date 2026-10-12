import argparse
import json
from pathlib import Path

import joblib
import pandas as pd
import torch
from torch import nn
from torch.utils.data import DataLoader

from ai_assistant_platform.ml.dataset import IntentDataset
from ai_assistant_platform.ml.intent_model import IntentClassifier
from ai_assistant_platform.ml.label_mapping import LabelMapping
from ai_assistant_platform.ml.preprocessing import IntentPreprocessor
from ai_assistant_platform.ml.training import evaluate_model, train_one_epoch


def main():
    # --- THÊM PHẦN NÀY ---
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", type=int, default=1, help="Số epoch cần huấn luyện")
    parser.add_argument("--batch-size", type=int, default=32, help="Kích thước batch")
    parser.add_argument("--lr", type=float, default=0.001, help="Learning rate")
    parser.add_argument(
        "--save-model", action="store_true", help="Lưu model sau khi train"
    )
    args = parser.parse_args()
    # ---------------------

    MODEL_PATH = Path("models/intent_classifier.pt")
    METADATA_PATH = Path("models/intent_metadata.json")

    TRAIN_DATA_PATH = Path("data/splits/train.csv")
    VALIDATION_DATA_PATH = Path("data/splits/validation.csv")
    df_train = pd.read_csv(TRAIN_DATA_PATH)
    df_validation = pd.read_csv(VALIDATION_DATA_PATH)

    # Trích xuất numeric & one-hot features
    preprocessor = IntentPreprocessor()
    X_train = preprocessor.fit_transform(
        df_train
    )  # Trả về ma trận numpy (N, n_features)
    X_validation = preprocessor.transform(df_validation)

    # Mã hóa chuỗi text intent thành số nguyên (0, 1, 2, ...)
    label_mapping = LabelMapping()
    label_mapping.fit(df_train["intent"])
    y_train = label_mapping.encode(df_train["intent"])
    y_validation = label_mapping.encode(df_validation["intent"])

    train_dataset = IntentDataset(X_train, y_train)
    validation_dataset = IntentDataset(X_validation, y_validation)
    train_loader = DataLoader(
        train_dataset,
        batch_size=args.batch_size,
        shuffle=True,  # Phải shuffle khi train
    )
    validation_loader = DataLoader(
        validation_dataset,
        batch_size=args.batch_size,
        shuffle=False,  # Không shuffle khi validation
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
        val_loss, val_metrics = evaluate_model(
            model=model,
            dataloader=validation_loader,
            criterion=criterion,
            device="cpu",
            labels=list(range(num_classes)),
        )
        print(
            f"Epoch {epoch}/{args.epochs} - "
            f"Train Loss: {avg_loss:.4f} - "
            f"Val Loss: {val_loss:.4f} - "
            f"Val Macro F1: {val_metrics['macro_f1']:.4f}"
        )

    if args.save_model:
        Path("models").mkdir(parents=True, exist_ok=True)
        torch.save(model.state_dict(), MODEL_PATH)

        metadata  = {
            "model_version": "torch_intent_v1",
            "input_dim": input_dim,
            "hidden_dim": 64,
            "num_classes": num_classes,
            "classes": list(label_mapping.classes_),
        }
        
        with open(METADATA_PATH, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        joblib.dump(preprocessor, "models/intent_preprocessor.joblib")


if __name__ == "__main__":
    main()
