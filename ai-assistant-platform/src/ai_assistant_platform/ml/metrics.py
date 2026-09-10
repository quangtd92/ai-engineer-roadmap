from collections.abc import Sequence
from typing import Any

import numpy as np
from sklearn.metrics import confusion_matrix, precision_recall_fscore_support


def calculate_confusion_matrix(
    y_true: Sequence[Any] | np.ndarray,
    y_pred: Sequence[Any] | np.ndarray,
    labels: Sequence[Any] | np.ndarray | None = None,
) -> np.ndarray:
    """Tính toán ma trận nhầm lẫn (confusion matrix) đa lớp.

    Args:
        y_true: Danh sách nhãn thực tế.
        y_pred: Danh sách nhãn mô hình dự đoán.
        labels: Danh sách thứ tự nhãn cố định. Đảm bảo kích thước ma trận là (C, C)
            ngay cả khi tập đánh giá thiếu một số class.

    Returns:
        np.ndarray: Ma trận 2D kích thước (C, C) với hàng là True và cột là Pred.
    """
    return confusion_matrix(y_true, y_pred, labels=labels)


def calculate_classification_metrics(
    y_true: Sequence[Any] | np.ndarray,
    y_pred: Sequence[Any] | np.ndarray,
    labels: Sequence[Any] | np.ndarray | None = None,
    target_names: Sequence[str] | None = None,
    zero_division: int | str = 0,
) -> dict[str, Any]:
    """Tính toán các chỉ số phân loại (precision, recall, f1, support) cho từng class và tổng thể.

    Args:
        y_true: Nhãn thực tế.
        y_pred: Nhãn dự đoán.
        labels: Danh sách các nhãn (class).
        target_names: Tên của các nhãn.
        zero_division: Giá trị trả về khi mẫu bằng 0.

    Returns:
        dict: Dictionary chứa các chỉ số phân loại.
    """
    precision, recall, f1, support = precision_recall_fscore_support(
        y_true, y_pred, labels=labels, zero_division=zero_division
    )

    macro_f1 = float(np.mean(f1))
    if np.sum(support) == 0:
        weighted_f1 = 0.0
    else:
        weighted_f1 = float(np.average(f1, weights=support))

    per_class = {
        "precision": precision.tolist(),
        "recall": recall.tolist(),
        "f1": f1.tolist(),
        "support": support.tolist()
    }

    return {
        "macro_f1": macro_f1,
        "weighted_f1": weighted_f1,
        "per_class": per_class
    }
