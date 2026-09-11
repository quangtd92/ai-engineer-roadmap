import argparse
import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

from ai_assistant_platform.ml.label_mapping import LabelMapping
from ai_assistant_platform.ml.metrics import (
    calculate_classification_metrics,
    calculate_confusion_matrix,
)
from ai_assistant_platform.ml.preprocessing import IntentPreprocessor

TRAIN_DATA_PATH = Path("data/splits/train.csv")
VALIDATION_DATA_PATH = Path("data/splits/validation.csv")
TEST_DATA_PATH = Path("data/splits/test.csv")
MODEL_OUTPUT_PATH = Path("models/sklearn_intent_baseline.joblib")
REPORT_OUTPUT_PATH = Path("docs/ml_evaluation_metrics.json")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Huấn luyện Logistic Regression Baseline cho Intent Classification"
    )
    parser.add_argument(
        "--write-report",
        action="store_true",
        help="Xuất kết quả đánh giá ra file docs/ml_evaluation_metrics.json",
    )
    parser.add_argument(
        "--evaluate-test",
        action="store_true",
        help="Đánh giá trên tập test",
    )
    args = parser.parse_args()
    print(f"{args=}")
    # return
    # 1. Tải dữ liệu
    df_train = pd.read_csv(TRAIN_DATA_PATH)
    df_validation = pd.read_csv(VALIDATION_DATA_PATH)
    if args.evaluate_test:
        df_test = pd.read_csv(TEST_DATA_PATH)

    # 2. Tiền xử lý đặc trưng
    intent_preprocessor = IntentPreprocessor()
    X_train = intent_preprocessor.fit_transform(df_train)
    X_validation = intent_preprocessor.transform(df_validation)
    if args.evaluate_test:
        X_test = intent_preprocessor.transform(df_test)

    # 3. Mã hóa nhãn (Label Encoding)
    label_mapping = LabelMapping()
    label_mapping.fit(df_train["intent"])
    y_train = label_mapping.encode(df_train["intent"])
    y_validation = label_mapping.encode(df_validation["intent"])
    if args.evaluate_test:
        y_test = label_mapping.encode(df_test["intent"])

    # 4. Huấn luyện mô hình
    model = LogisticRegression(max_iter=1000, random_state=42)
    model.fit(X_train, y_train)

    # 5. Đánh giá trên tập Validation
    y_val_pred = model.predict(X_validation)
    acc_val = accuracy_score(y_validation, y_val_pred)

    if args.evaluate_test:
        # 6. Đánh giá trên tập Test
        y_test_pred = model.predict(X_test)
        acc_test = accuracy_score(y_test, y_test_pred)

    classes = list(range(len(label_mapping.classes_)))
    class_names = [str(c) for c in label_mapping.classes_]

    cm = calculate_confusion_matrix(y_validation, y_val_pred, labels=classes)
    metrics = calculate_classification_metrics(y_validation, y_val_pred, labels=classes)

    if args.evaluate_test:
        cm_test = calculate_confusion_matrix(y_test, y_test_pred, labels=classes)
        metrics_test = calculate_classification_metrics(
            y_test, y_test_pred, labels=classes
        )

    print(f"y_val_pred: {y_val_pred}")
    print(f"Accuracy: {acc_val:.4f}")
    print(f"Macro F1: {metrics['macro_f1']:.4f}")
    print(f"Weighted F1: {metrics['weighted_f1']:.4f}")
    print(f"\nConfusion Matrix (labels={class_names}):\n{cm}")

    # In chi tiết từng class ra console
    print("\nPer-Class Metrics (Validation):")
    per_class = metrics["per_class"]
    print(f"{'Class':<30} {'Precision':<10} {'Recall':<10} {'F1':<10} {'Support':<8}")
    print("-" * 68)
    for i, name in enumerate(class_names):
        p = per_class["precision"][i]
        r = per_class["recall"][i]
        f = per_class["f1"][i]
        s = per_class["support"][i]
        print(f"{name:<30} {p:<10.4f} {r:<10.4f} {f:<10.4f} {s:<8}")

    if args.evaluate_test:
        print("\n" + "=" * 30 + " Test Set Evaluation " + "=" * 30)
        print(f"y_test_pred: {y_test_pred}")
        print(f"Accuracy (Test): {acc_test:.4f}")
        print(f"Macro F1 (Test): {metrics_test['macro_f1']:.4f}")
        print(f"Weighted F1 (Test): {metrics_test['weighted_f1']:.4f}")
        print(f"\nConfusion Matrix (labels={class_names}):\n{cm_test}")
        print("\nPer-Class Metrics (Test):")
        per_class_test = metrics_test["per_class"]
        print(
            f"{'Class':<30} {'Precision':<10} {'Recall':<10} {'F1':<10} {'Support':<8}"
        )
        print("-" * 68)
        for i, name in enumerate(class_names):
            p = per_class_test["precision"][i]
            r = per_class_test["recall"][i]
            f = per_class_test["f1"][i]
            s = per_class_test["support"][i]
            print(f"{name:<30} {p:<10.4f} {r:<10.4f} {f:<10.4f} {s:<8}")

    # 6. Lưu model artifact
    MODEL_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    artifacts = {
        "preprocessor": intent_preprocessor,
        "model": model,
        "label_mapping": label_mapping,
        "model_version": "sklearn_intent_v1",
    }
    joblib.dump(artifacts, MODEL_OUTPUT_PATH)
    print(f"\nModel artifact saved to {MODEL_OUTPUT_PATH}")

    # 7. Xuất file JSON nếu có cờ --write-report
    if args.write_report:
        report_payload = {
            "validate": {
                "model": "LogisticRegression",
                "accuracy": round(float(acc_val), 4),
                "macro_f1": round(float(metrics["macro_f1"]), 4),
                "weighted_f1": round(float(metrics["weighted_f1"]), 4),
                "per_class": {
                    name: {
                        "precision": round(float(per_class["precision"][i]), 4),
                        "recall": round(float(per_class["recall"][i]), 4),
                        "f1": round(float(per_class["f1"][i]), 4),
                        "support": int(per_class["support"][i]),
                    }
                    for i, name in enumerate(class_names)
                },
            }
        }

        if args.evaluate_test:
            report_payload["test"] = {
                "accuracy_test": round(float(acc_test), 4),
                "macro_f1_test": round(float(metrics_test["macro_f1"]), 4),
                "weighted_f1_test": round(float(metrics_test["weighted_f1"]), 4),
                "per_class_test": {
                    name: {
                        "precision": round(float(per_class_test["precision"][i]), 4),
                        "recall": round(float(per_class_test["recall"][i]), 4),
                        "f1": round(float(per_class_test["f1"][i]), 4),
                        "support": int(per_class_test["support"][i]),
                    }
                    for i, name in enumerate(class_names)
                },
            }

        REPORT_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(REPORT_OUTPUT_PATH, "w", encoding="utf-8") as f:
            json.dump(report_payload, f, indent=2, ensure_ascii=False)
        print(f"Metrics report exported to {REPORT_OUTPUT_PATH}")


if __name__ == "__main__":
    main()
