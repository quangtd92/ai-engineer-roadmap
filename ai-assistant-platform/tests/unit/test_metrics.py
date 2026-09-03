import numpy as np

from ai_assistant_platform.ml.metrics import calculate_confusion_matrix


def test_confusion_matrix_shape_and_values():
    y_true = [0, 1, 0, 1, 2, 2]
    y_pred = [0, 0, 1, 1, 2, 2]
    labels = [0, 1, 2]

    cm = calculate_confusion_matrix(y_true, y_pred, labels=labels)

    expected = np.array([
        [1, 1, 0],
        [1, 1, 0],
        [0, 0, 2],
    ])
    assert cm.shape == (3, 3)
    np.testing.assert_array_equal(cm, expected)


def test_confusion_matrix_fixed_labels_order():
    y_true = [0, 1, 0, 1, 2, 2]
    y_pred = [0, 0, 1, 1, 2, 2]
    labels = [0, 1, 2, 3]

    cm = calculate_confusion_matrix(y_true, y_pred, labels=labels)

    expected = np.array([
        [1, 1, 0, 0],
        [1, 1, 0, 0],
        [0, 0, 2, 0],
        [0, 0, 0, 0],
    ])
    assert cm.shape == (4, 4)
    np.testing.assert_array_equal(cm, expected)
