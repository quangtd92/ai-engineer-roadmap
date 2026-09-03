from collections.abc import Sequence
from typing import Any

import numpy as np
from sklearn.metrics import confusion_matrix


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
