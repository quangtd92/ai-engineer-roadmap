import numpy as np

from ai_assistant_platform.ml.metrics import (
    calculate_classification_metrics,
    calculate_confusion_matrix,
)


def test_confusion_matrix_shape_and_values():
    y_true = [0, 1, 0, 1, 2, 2]
    y_pred = [0, 0, 1, 1, 2, 2]
    labels = [0, 1, 2]

    cm = calculate_confusion_matrix(y_true, y_pred, labels=labels)

    expected = np.array(
        [
            [1, 1, 0],
            [1, 1, 0],
            [0, 0, 2],
        ]
    )
    assert cm.shape == (3, 3)
    np.testing.assert_array_equal(cm, expected)


def test_confusion_matrix_fixed_labels_order():
    y_true = [0, 1, 0, 1, 2, 2]
    y_pred = [0, 0, 1, 1, 2, 2]
    labels = [0, 1, 2, 3]

    cm = calculate_confusion_matrix(y_true, y_pred, labels=labels)

    expected = np.array(
        [
            [1, 1, 0, 0],
            [1, 1, 0, 0],
            [0, 0, 2, 0],
            [0, 0, 0, 0],
        ]
    )
    assert cm.shape == (4, 4)
    np.testing.assert_array_equal(cm, expected)


def test_classification_metrics():
    y_true = [0, 1, 0, 1]
    y_pred = [0, 0, 1, 1]
    labels = [0, 1]

    metrics = calculate_classification_metrics(y_true, y_pred, labels=labels)

    expected = {
        "macro_f1": 0.5,
        "weighted_f1": 0.5,
        "per_class": {
            "precision": [0.5, 0.5],
            "recall": [0.5, 0.5],
            "f1": [0.5, 0.5],
            "support": [2, 2],
        },
    }

    assert metrics == expected
