# Kế Hoạch Huấn Luyện Mô Hình Học Sâu PyTorch (Week-03 Training Plan)

Tài liệu này xác lập bản đặc tả kỹ thuật và kế hoạch chuyển giao (handoff) từ mô hình Baseline Scikit-learn (Tuần 2) sang Mạng Nơ-ron PyTorch (Tuần 3) cho bài toán Phân loại Ý định Người dùng (Intent Classification) trong `ai-assistant-platform`.

---

## 1. Bối Cảnh & Mục Tiêu Chuyển Giao (Handoff Context)

### 1.1. Hiện trạng sau Tuần 2 (Scikit-learn Baseline)
- **Mô hình**: `LogisticRegression(max_iter=1000, random_state=42)` kết hợp bộ tiền xử lý heuristic `IntentPreprocessor`.
- **Đặc trưng**: 6 chiều đặc trưng hình thức (`text_length`, `word_count`, `has_question_marks`, và 3 chiều One-Hot của `source`).
- **Hiệu năng cơ sở (Baseline Benchmark)**:
  - **Validation Set (8 mẫu)**: Accuracy = `0.1250`, Macro F1 = `0.1333`, Weighted F1 = `0.1667`.
  - **Held-out Test Set (7 mẫu)**: Accuracy = `0.4286`, Macro F1 = `0.4133`, Weighted F1 = `0.4476`.
- **Hạn chế cốt lõi**:
  - Mô hình bị thiên lệch dự đoán (prediction bias) dồn vào `intent.create_meeting` và `intent.send_email`.
  - Hai intent quan trọng là `intent.daily_schedule` và `intent.search_file` hoàn toàn thất bại (F1 = 0.0000) do đặc trưng độ dài không chứa thông tin ngữ nghĩa.

### 1.2. Mục tiêu Tuần 3
- Chuyển đổi toàn bộ quy trình sang framework **PyTorch**.
- Xây dựng `Dataset`, `DataLoader`, kiến trúc mạng nơ-ron đa tầng (MLP), và chu trình huấn luyện (training loop/validation loop) chuẩn mực.
- Thiết lập chuẩn so sánh công bằng: Mô hình PyTorch phải vượt qua mốc Macro F1 cơ sở (`0.1333`) của Tuần 2 trên cùng tập Validation.

---

## 2. Đặc Tả Kỹ Thuật Dữ Liệu (Tensor Specifications)

### 2.1. Tensor Đặc Trưng Đầu Vào (Input Features Tensor)
- **Nguồn trích xuất**: Sử dụng đối tượng [IntentPreprocessor](/ai-assistant-platform/src/ai_assistant_platform/ml/preprocessing.py) đã `fit` trên tập Train (`data/splits/train.csv`).
- **Số chiều (Dimensions)**: Tensor 2D kích thước `(batch_size, 6)`.
  - 3 đặc trưng số đã qua `StandardScaler`: độ dài ký tự, số từ, cờ chứa dấu `?`.
  - 3 đặc trưng phân loại qua `OneHotEncoder`: `source` thuộc `[app_desktop, phone, web_ui]`.
- **Kiểu dữ liệu (Dtype)**: `torch.float32` (bắt buộc đối với các phép tính nhân ma trận trong `nn.Linear`).

### 2.2. Tensor Nhãn Mục Tiêu (Target Label Tensor)
- **Nguồn ánh xạ**: Sử dụng đối tượng [LabelMapping](/ai-assistant-platform/src/ai_assistant_platform/ml/label_mapping.py) đã fit trên tập Train.
- **Thứ tự nhãn cố định (5 lớp)**:
  - `0`: `intent.create_document`
  - `1`: `intent.create_meeting`
  - `2`: `intent.daily_schedule`
  - `3`: `intent.search_file`
  - `4`: `intent.send_email`
- **Số chiều (Dimensions)**: Tensor 1D kích thước `(batch_size,)`.
- **Kiểu dữ liệu (Dtype)**: `torch.long` (yêu cầu chuẩn của `torch.nn.CrossEntropyLoss` cho bài toán phân loại đa lớp).

---

## 3. Tiêu Chuẩn Đối Sánh Chỉ Số (Metrics & Passing Criteria)

Để đảm bảo tính nhất quán giữa hai tuần, hệ thống chỉ số đánh giá được giữ nguyên:

| Chỉ số | Vai trò | Mục tiêu tối thiểu cần đạt ở Tuần 3 |
| :--- | :--- | :--- |
| **Macro F1** | **Chỉ số chính (Primary Metric)** | Phải vượt mốc **`> 0.1333`** trên Validation Set. Đảm bảo đánh giá công bằng 5 intent độc lập. |
| **Accuracy** | Chỉ số phụ | Theo dõi tỷ lệ đoán đúng tổng thể (Baseline Validation là `12.5%`). |
| **Per-Class F1** | Kiểm tra phân phối lỗi | Giảm thiểu số lớp bị F1 = 0.0000 (Baseline bị 4/5 lớp F1 = 0). |
| **Confusion Matrix** | Phân tích trực quan | Đánh giá trực quan hiện tượng nhầm lẫn giữa các cặp nhãn. |

---

## 4. Thiết Kế Kiến Trúc Mạng Nơ-ron Dự Kiến (Neural Network Design)

- **Class kế thừa**: `torch.nn.Module` (đặt tại `src/ai_assistant_platform/ml/intent_model.py`).
- **Dạng mạng**: Multi-Layer Perceptron (MLP) nhỏ gọn, phù hợp với tập dữ liệu kích thước khiêm tốn:
  ```text
  Input (batch_size, 6)
       │
       ▼
  Linear(in_features=6, out_features=16)
       │
       ▼
  ReLU()
       │
       ▼
  Dropout(p=0.2)  [Tùy chọn chống overfit]
       │
       ▼
  Linear(in_features=16, out_features=5)
       │
       ▼
  Raw Logits (batch_size, 5)
  ```
- **Lưu ý kiến trúc**:
  - Không đặt lớp `Softmax` ở cuối mô hình vì `nn.CrossEntropyLoss` đã kết hợp sẵn `LogSoftmax` và `NLLLoss` để đảm bảo ổn định số học (numerical stability).
  - Khi suy luận (inference), sử dụng `torch.softmax(logits, dim=-1)` để trích xuất `confidence`.

---

## 5. Lộ Trình Triển Khai Chi Tiết (Tuần 3)

| Ngày | Module / File cần tạo hoặc sửa | Trọng tâm công việc |
| :---: | :--- | :--- |
| **Ngày 15** | `src/ai_assistant_platform/ml/dataset.py`<br>`tests/unit/test_intent_dataset.py` | Viết class `IntentDataset(Dataset)`; đảm bảo trả về tuple `(features, label)` đúng dtype `float32` và `long`. |
| **Ngày 16** | `src/ai_assistant_platform/ml/dataset.py`<br>`scripts/check_intent_dataloader.py`<br>`tests/unit/test_intent_dataloader.py` | Tạo hàm `create_intent_dataloaders()`; kiểm tra batch size, shuffle ở train và không shuffle ở val. |
| **Ngày 17** | `src/ai_assistant_platform/ml/intent_model.py`<br>`tests/unit/test_intent_model.py` | Định nghĩa class mạng nơ-ron; kiểm tra forward pass với batch giả định `(batch_size, 6) -> (batch_size, 5)`. |
| **Ngày 18** | `scripts/train_torch_intent.py` | Viết training loop & validation loop hoàn chỉnh; tính loss và classification metrics sau mỗi epoch; lưu artifact `models/intent_classifier.pt`. |
| **Ngày 19** | `src/ai_assistant_platform/services/intent_service.py`<br>`tests/unit/test_intent_service.py` | Viết service wrapper cho mô hình PyTorch; chuyển model sang `eval()` mode và dùng `torch.no_grad()`. |
| **Ngày 20** | `src/ai_assistant_platform/api/routes/ml.py`<br>`tests/integration/test_ml_router.py` | Tạo FastAPI router phục vụ endpoint `/api/v1/ml/predict-intent`. |
| **Ngày 21** | `docs/ml-evaluation-report.md` | Bổ sung phần so sánh PyTorch vs Scikit-learn Baseline; chốt milestone Tuần 3. |

---

## 6. Rủi Ro Kỹ Thuật & Biện Pháp Giảm Thiểu

1. **Nguy cơ Overfitting cao do dữ liệu nhỏ**:
   - *Biện pháp*: Giữ số lượng tham số mô hình nhỏ (`hidden_dim = 16` hoặc `32`), sử dụng `weight_decay` trong Adam optimizer, và theo dõi Validation Loss để dừng đúng lúc (Early Stopping).
2. **Class Imbalance trong mini-batch**:
   - *Biện pháp*: Do tập train chỉ có 37 mẫu, chọn `batch_size` hợp lý (ví dụ: 8 hoặc 16) để mỗi batch đại diện tương đối cho các lớp.
3. **Reproducibility (Tính tái lập kết quả)**:
   - *Biện pháp*: Cố định seed ngẫu nhiên cho cả NumPy và PyTorch (`torch.manual_seed(42)`).
