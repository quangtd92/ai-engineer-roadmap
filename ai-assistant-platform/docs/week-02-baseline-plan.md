# Kế hoạch Huấn luyện Mô hình Baseline (Tháng 2 - Tuần 2)

Tài liệu này đặc tả kỹ thuật và kế hoạch triển khai mô hình học máy cơ sở (Baseline ML) cho tính năng **Intent Classification** của `ai-assistant-platform`.

---

## 1. Tổng quan Dữ liệu (Dataset Overview)

Dữ liệu được xử lý qua data pipeline ở Tuần 1 và phân tách thành 3 tập split độc lập (tỷ lệ xấp xỉ 70/15/15, có phân tầng theo `intent`):

- **Tập Train (`data/splits/train.csv`)**: Dùng để huấn luyện mô hình và fit preprocessor.
- **Tập Validation (`data/splits/validation.csv`)**: Dùng để tinh chỉnh threshold, phân tích lỗi (error analysis) và chọn mô hình.
- **Tập Test (`data/splits/test.csv`)**: Dữ liệu held-out độc lập, chỉ đánh giá một lần duy nhất khi chốt mô hình baseline.

### Danh sách Intent (5 classes)
1. `intent.daily_schedule`: Truy vấn lịch trình, thời gian biểu cá nhân.
2. `intent.create_meeting`: Yêu cầu tạo/đặt lịch cuộc họp.
3. `intent.send_email`: Yêu cầu soạn, gửi thư hoặc phản hồi email.
4. `intent.search_file`: Tìm kiếm tệp tin, tài liệu hoặc hợp đồng.
5. `intent.create_document`: Khởi tạo văn bản, tài liệu, file ghi chú mới.

---

## 2. Đặc tả Feature Matrix ($X$)

Đầu vào cho mô hình được trích xuất và biến đổi qua `IntentPreprocessor`:

| Feature Name | Kiểu Dữ Liệu | Tiền Xử Lý / Encoding | Mô Tả |
| :--- | :--- | :--- | :--- |
| `text_length` | Numeric (`int32`) | `StandardScaler` | Số ký tự của câu input (`len(text)`). |
| `word_count` | Numeric (`int32`) | `StandardScaler` | Số từ trong câu (`len(text.split())`). |
| `has_question_mark` | Numeric (`int32`) | `StandardScaler` | Cờ nhị phân (1 nếu chứa `?`, 0 nếu không). |
| `source` | Categorical (`str`) | `OneHotEncoder(handle_unknown='ignore')` | Nền tảng gửi request (`app_desktop`, `web_ui`, `phone`). |

- **Output Matrix**: `np.ndarray` với `dtype=np.float32`.
- **Ràng buộc Data Leakage**: `IntentPreprocessor` chỉ được gọi `fit(df_train)` trên tập train; các tập validation và test chỉ gọi `transform()`.

---

## 3. Quy tắc Mã hóa Nhãn (Label Mapping - $y$)

Nhãn chuỗi văn bản (`intent`) được ánh xạ thành số nguyên (`int64`) phục vụ thuật toán phân loại đa lớp (Multi-class Classification):

```python
LABEL_TO_ID = {
    "intent.create_document": 0,
    "intent.create_meeting": 1,
    "intent.daily_schedule": 2,
    "intent.search_file": 3,
    "intent.send_email": 4,
}

ID_TO_LABEL = {v: k for k, v in LABEL_TO_ID.items()}
```

- Thứ tự nhãn được cố định theo bảng chữ cái để đảm bảo tính nhất quán khi sinh **Confusion Matrix** và **Classification Report**.

---

## 4. Kiến trúc Mô hình Baseline

- **Thuật toán chính**: `LogisticRegression` từ thư viện `scikit-learn`.
- **Cấu hình mặc định**:
  - `multi_class="multinomial"` (hoặc `"auto"`)
  - `solver="lbfgs"`
  - `random_state=42`
  - `max_iter=1000`
- **Mục đích**:
  - Làm thước đo chuẩn (benchmark) nhanh, nhẹ, có khả năng giải thích (interpretable).
  - So sánh hiệu năng với mô hình Deep Learning (PyTorch MLP / Neural Network) ở Tuần 3.

---

## 5. Chiến lược Đánh giá (Evaluation Strategy)

### 5.1. Metrics chính
Không sử dụng đơn lẻ chỉ số **Accuracy** do kích thước tập dữ liệu nhỏ và cần kiểm soát lỗi từng class. Các metrics bắt buộc gồm:

1. **Confusion Matrix**: Ma trận nhầm lẫn kích thước $5 \times 5$ xác định rõ cặp nhãn hay bị dự đoán sai.
2. **Per-class Precision, Recall, F1-score**: Đánh giá chi tiết năng lực nhận diện của từng intent.
3. **Macro F1-score**: Metric tổng hợp chính (đánh giá đồng đều tất cả các class bất kể số lượng mẫu).
4. **Weighted F1-score**: Metric tổng hợp có tính đến trọng số phân bố mẫu.

### 5.2. Quy trình Đánh giá
1. **Huấn luyện & Validation (Ngày 9 - 11)**:
   - Fit mô hình trên `train.csv`.
   - Dự đoán và phân tích lỗi trên `validation.csv`.
   - Xuất báo cáo sơ bộ vào `docs/ml-evaluation-report.md`.
2. **Đóng gói Service (Ngày 12)**:
   - Đóng gói mô hình và preprocessor thành `IntentBaselineService` có caching artifact.
3. **Đánh giá Test Set (Ngày 13)**:
   - Chạy cờ `--evaluate-test` một lần duy nhất trên `test.csv` để chốt kết quả milestone.

---

## 6. Lộ trình Thực hiện (Tuần 2)

- **Ngày 8**: Tìm hiểu Supervised Learning & Toy Linear Regression.
- **Ngày 9**: Huấn luyện `LogisticRegression` (`scripts/train_sklearn_baseline.py`).
- **Ngày 10**: Bổ sung `Confusion Matrix` (`src/ai_assistant_platform/ml/metrics.py`).
- **Ngày 11**: Hoàn thiện báo cáo Precision, Recall, F1 (`docs/ml-evaluation-report.md`).
- **Ngày 12**: Đóng gói `IntentBaselineService` (`src/ai_assistant_platform/services/intent_baseline_service.py`).
- **Ngày 13**: Milestone evaluation trên Test set.
- **Ngày 14**: Review, dọn dẹp và lập kế hoạch chuyển giao sang PyTorch (Tuần 3).
