

from pathlib import Path

import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

from ai_assistant_platform.ml.label_mapping import LabelMapping
from ai_assistant_platform.ml.preprocessing import IntentPreprocessor

TRAIN_DATA_PATH = Path("data/splits/train.csv")
VALIDATION_DATA_PATH = Path("data/splits/validation.csv")
MODEL_OUTPUT_PATH = Path("models/sklearn_intent_baseline.joblib")


def main():
    df_train = pd.read_csv(TRAIN_DATA_PATH)
    df_validation = pd.read_csv(VALIDATION_DATA_PATH)
    
    intent_preprocessor = IntentPreprocessor()
    X_train = intent_preprocessor.fit_transform(df_train)
    X_validation = intent_preprocessor.transform(df_validation)
    # print(f"X_train {X_train}")

    # print(f"df_train[intent] {df_train['intent']}")

    label_mapping = LabelMapping()
    label_mapping.fit(df_train["intent"])
    y_train = label_mapping.encode(df_train["intent"])
    y_validation = label_mapping.encode(df_validation["intent"])
    # print(f"y_train {y_train}")
    # print(f"y_validation {y_validation}")

    model = LogisticRegression(max_iter=1000, random_state=42)
    model.fit(X_train, y_train)
    y_val_pred = model.predict(X_validation)
    print(f"y_val_pred {y_val_pred}")

    acc = accuracy_score(y_validation, y_val_pred)
    print(f"Accuracy: {acc}")

    # Tạo thư mục models/ nếu chưa tồn tại
    MODEL_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Đóng gói cả 3 thành phần
    artifacts = {
        "preprocessor": intent_preprocessor,
        "model": model,
        "label_mapping": label_mapping,
    }

    # Lưu xuống ổ đĩa
    joblib.dump(artifacts, MODEL_OUTPUT_PATH)
    print(f"Model artifact saved to {MODEL_OUTPUT_PATH}")


if __name__ == "__main__":
    main()