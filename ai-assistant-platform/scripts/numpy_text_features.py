import sys
from pathlib import Path

import numpy as np
import pandas as pd

if hasattr(sys.stdout, "reconfigure") and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

DATA_PATH = Path("data/raw/intent_samples.csv")


def extract_features_from_texts(texts: list[str]) -> tuple[np.ndarray, list[str]]:
    """Trích xuất 3 feature numeric đơn giản từ danh sách text sử dụng NumPy array.

    Features:
    1. text_length: Độ dài chuỗi (số ký tự)
    2. word_count: Số từ trong câu (tách theo khoảng trắng)
    3. has_question_mark: Cờ 1 nếu có dấu hỏi '?', ngược lại 0
    """
    # Xử lý text rỗng hoặc None an toàn
    cleaned_texts = [str(t) if pd.notna(t) else "" for t in texts]

    # 1. Trích xuất đặc trưng
    text_lengths = np.array([len(t) for t in cleaned_texts], dtype=np.int32)
    word_counts = np.array([len(t.split()) for t in cleaned_texts], dtype=np.int32)
    has_question_marks = np.array(
        ["?" in t for t in cleaned_texts], dtype=np.int32
    )

    # 2. Ghép các vector 1D thành ma trận đặc trưng 2D (n_samples, n_features)
    # np.column_stack xếp các mảng 1D thành các cột của ma trận 2D
    feature_matrix = np.column_stack(
        [text_lengths, word_counts, has_question_marks]
    ).astype(np.float32)

    feature_names = ["text_length", "word_count", "has_question_mark"]
    return feature_matrix, feature_names


def main():
    if not DATA_PATH.exists():
        print(f"Lỗi: Không tìm thấy file dữ liệu tại {DATA_PATH}")
        return

    # Đọc dữ liệu thô
    df = pd.read_csv(DATA_PATH)
    texts = df["text"].tolist()
    # Trích xuất ma trận đặc trưng
    X, feature_names = extract_features_from_texts(texts)

    print("=" * 60)
    print("NUMPY SHAPE, DTYPE & VECTORIZATION CHO TEXT FEATURES")
    print("=" * 60)

    # 1. Kiểm tra shape, dtype, ndim
    print("\n[1] Thông tin Ma trận Feature X:")
    print(f"  - Shape (n_samples, n_features): {X.shape}")
    print(f"  - Số dòng (samples)   : {X.shape[0]}")
    print(f"  - Số cột (features)   : {X.shape[1]}")
    print(f"  - Dtype               : {X.dtype}")
    print(f"  - Số chiều (ndim)     : {X.ndim}")
    print(f"  - Dung lượng bộ nhớ   : {X.nbytes} bytes")
    print(f"  - Danh sách features  : {feature_names}")

    # 2. Vectorized aggregation theo trục (axis)
    # axis=0: tính toán dọc theo các dòng (trên toàn bộ sample cho mỗi feature)
    # axis=1: tính toán ngang theo các cột (trên từng sample)
    means = np.mean(X, axis=0)
    stds = np.std(X, axis=0)
    mins = np.min(X, axis=0)
    maxs = np.max(X, axis=0)

    print("\n[2] Thống kê Vectorized Aggregation (axis=0):")
    for idx, name in enumerate(feature_names):
        print(
            f"  - {name:18}: Mean={means[idx]:6.2f} | Std={stds[idx]:5.2f} | Min={mins[idx]:4.1f} | Max={maxs[idx]:4.1f}"
        )

    # 3. Vectorized operations & Boolean masking
    # Tìm các câu hỏi (feature has_question_mark == 1) mà không dùng vòng lặp
    is_question = X[:, 2] == 1.0
    question_count = np.sum(is_question)
    long_sentences = X[:, 0] > means[0]
    long_sentence_count = np.sum(long_sentences)

    print("\n[3] Vectorized Boolean Filtering:")
    print(f"  - Tổng số câu hỏi (?): {question_count}/{X.shape[0]}")
    print(
        f"  - Số câu dài hơn độ dài trung bình ({means[0]:.1f} ký tự): {long_sentence_count}/{X.shape[0]}"
    )

    # 4. Hiển thị mẫu 5 dòng đầu tiên cùng text gốc
    print("\n[4] Mẫu 5 dòng đầu tiên (Text -> Feature Vector):")
    print(f"  {'ID':<4} | {'Text':<45} | {'Features [len, words, ?]':<25}")
    print("  " + "-" * 78)
    for i in range(min(5, len(texts))):
        raw_text = str(texts[i]) if pd.notna(texts[i]) else "<EMPTY>"
        if len(raw_text) > 42:
            raw_text = raw_text[:39] + "..."
        feat_repr = f"[{X[i, 0]:4.0f}, {X[i, 1]:2.0f}, {X[i, 2]:1.0f}]"
        print(f"  {i+1:<4} | {raw_text:<45} | {feat_repr}")

    print("\n" + "=" * 60)
    print("Xác nhận hoàn thành:")
    print(f"  X.shape == ({X.shape[0]}, 3) -> Đúng định dạng 2D matrix cho model input.")
    print(f"  X.dtype == {X.dtype} -> Kiểu số thuần túy, tương thích PyTorch/scikit-learn.")
    print("=" * 60)

    
    # 1. Gán lại kết quả fillna để tránh lỗi NaN
    text_series = df["text"].fillna("")

    # 2. Vectorized operations bằng Pandas string accessor (.str)
    text_lengths = text_series.str.len()
    word_counts = text_series.str.split().str.len()
    has_question_marks = text_series.str.contains("?", regex=False).astype(int)

    # 3. Chuyển sang ma trận NumPy 2D
    Y = np.column_stack([text_lengths, word_counts, has_question_marks]).astype(np.float32)


if __name__ == "__main__":
    main()
