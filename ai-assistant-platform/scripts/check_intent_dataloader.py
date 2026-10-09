import numpy as np

from ai_assistant_platform.ml.dataset import IntentDataset, create_intent_dataloaders


def main():
    # 1. Tạo giả lập X (features) và y (labels) cho tập train (10 mẫu, 2 features)
    X_train = np.array(
        [
            [1.0, 2.0],
            [3.0, 4.0],
            [5.0, 6.0],
            [7.0, 8.0],
            [9.0, 10.0],
            [11.0, 12.0],
            [13.0, 14.0],
            [15.0, 16.0],
            [17.0, 18.0],
            [19.0, 20.0],
        ]
    )
    y_train = np.array([0, 1, 0, 1, 0, 1, 0, 1, 0, 1])  # 10 nhãn tương ứng

    # 2. Tạo giả lập X và y cho tập validation (4 mẫu, 2 features)
    X_val = np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0], [7.0, 8.0]])
    y_val = np.array([0, 1, 0, 1])  # 4 nhãn tương ứng

    # 3. Tạo đối tượng IntentDataset cho train và val
    train_dataset = IntentDataset(X_train, y_train)
    val_dataset = IntentDataset(X_val, y_val)

    # 4. Khởi tạo DataLoaders với batch_size=2
    train_loader, val_loader = create_intent_dataloaders(
        train_dataset, val_dataset, batch_size=2
    )

    # 5. Kiểm tra duyệt qua các batch
    print("--- TRAIN LOADER BATCHES ---")
    for batch_idx, (features, labels) in enumerate(train_loader, start=1):
        print(
            f"Batch {batch_idx}: features.shape={features.shape}, labels.shape={labels.shape}"
        )

    print("\n--- VAL LOADER BATCHES ---")
    for batch_idx, (features, labels) in enumerate(val_loader, start=1):
        print(
            f"Batch {batch_idx}: features.shape={features.shape}, labels.shape={labels.shape}"
        )


if __name__ == "__main__":
    main()
