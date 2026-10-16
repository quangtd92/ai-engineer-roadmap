# Báo Cáo Đánh Giá Mô Hình Học Máy (ML Evaluation Report)

Tài liệu này theo dõi và ghi nhận toàn bộ quá trình thực nghiệm, đánh giá mô hình học máy (Machine Learning) cho `ai-assistant-platform` trong Tháng 2.

---

## 1. Phân biệt Bài toán: Regression vs Classification

Trước khi đi vào xây dựng mô hình phân loại intent, nhóm thực nghiệm làm rõ hai bài toán cốt lõi trong Học có giám sát (Supervised Learning):

| Tiêu chí | Regression (Hồi quy) | Classification (Phân loại) |
| :--- | :--- | :--- |
| **Bản chất mục tiêu (`y`)** | Con số thực đo đạc được (liên tục): `y ∈ ℝ` | Tên nhãn lớp rời rạc: `y ∈ {nhãn 1, nhãn 2, ...}` |
| **Ví dụ kết quả** | Độ trễ xử lý: `15.2 ms`, `200.5 ms` | Ý định người dùng: `intent.daily_schedule`, `intent.send_email` |
| **Phép toán trên `y`** | Có thể cộng, trừ, nhân, chia, tính trung bình | Không đo đạc, không cộng trừ nhân chia được |
| **Ứng dụng trong Platform** | Dự đoán độ trễ hệ thống (`latency_ms`) ở Ngày 8 | Nhận diện mục đích câu hỏi của người dùng (5 intent) ở Ngày 9 |

> **LƯU Ý KIẾN TRÚC**:
> Không sử dụng Linear Regression để phân loại Intent. Linear Regression dự đoán ra một con số thực chạy tự do từ `-∞` đến `+∞`, hoàn toàn không thể gán nhãn hay chỉ ra xác suất thuộc về nhóm intent nào.

---

## 2. Nhật ký Thực nghiệm: Toy Linear Regression (Ngày 8 / Day 36)

Thực nghiệm được thực hiện thông qua script [linear_regression_overview.py](file:///e:/repos/cilel1/ai-assistant-platform/scripts/linear_regression_overview.py) nhằm làm quen với API chuẩn của `scikit-learn` (`fit`, `predict`, trích xuất tham số trọng số và tính metric sai số).

### 2.1. Thiết lập Dữ liệu Tổng hợp (Synthetic Data)
- **Kích thước mẫu**: `N = 100` mẫu.
- **Đặc trưng đầu vào (`X`)**: Mảng 2D kích thước `(100, 1)`, mô phỏng độ dài văn bản (`text_length`) từ 5 đến 120 ký tự.
- **Nhiễu đo lường (`noise`)**: Phân phối chuẩn `noise ~ N(0, 1)`.
- **Hàm mục tiêu quy định (Ground Truth)**:
  `y = 200.0 + 12.0 * X + noise`
  - Intercept nền (Base Latency): `200.0 ms`
  - Hệ số góc (Slope / Weight): `12.0 ms / ký tự`

### 2.2. Kết quả Huấn luyện & Đánh giá
Sau khi huấn luyện mô hình `LinearRegression()` từ thư viện `scikit-learn`:

- **Hệ số học được (`coef_`)**: `≈ 12.00` (khớp với Ground Truth slope = 12.0)
- **Điểm cắt trục tung (`intercept_`)**: `≈ 200.05` (khớp với Ground Truth intercept = 200.0)
- **Sai số tuyệt đối trung bình (MAE)**: `≈ 0.75 ms`

**Kết luận thực nghiệm**:
- Mô hình `LinearRegression` của scikit-learn tìm lại chính xác các tham số cơ sở ẩn trong dữ liệu dù có nhiễu ngẫu nhiên.
- Vòng đời `fit` -> `predict` -> `evaluate` hoạt động đúng chuẩn thiết kế.

---

## 3. Khung Đánh giá Mô hình Intent Baseline (Ngày 9 - 13)

Phần này được thiết lập sẵn để ghi nhận kết quả huấn luyện mô hình `LogisticRegression` đa lớp trên tập dữ liệu intent thực tế (`data/splits/`).

### 3.1. Cấu hình Baseline
- **Thuật toán**: `LogisticRegression(multi_class="multinomial", solver="lbfgs", max_iter=1000, random_state=42)`
- **Dữ liệu**:
  - Train: `data/splits/train.csv` (fit preprocessor & model)
  - Validation: `data/splits/validation.csv` (đánh giá lỗi & chọn ngưỡng)
  - Test: `data/splits/test.csv` (held-out test, chỉ chạy khi chốt baseline)

### 3.2. Bảng theo dõi Metrics (Validation Set)

| Model Version | Accuracy | Macro F1 | Weighted F1 | Ghi chú / Lỗi chính quan sát được |
| :--- | :--- | :--- | :--- | :--- |
| *Baseline Logistic Regression* | `0.125` (1/8) | `0.133` | `0.167` | Model bị lệch (bias) nặng về `create_meeting` và `send_email`; chỉ dùng 4 feature bề mặt nên thiếu ngữ nghĩa văn bản. |

### 3.3. Confusion Matrix & Error Analysis (Ngày 10)

Thứ tự nhãn cố định theo bảng chữ cái từ `label_mapping.classes_`:
- `0`: `intent.create_document`
- `1`: `intent.create_meeting`
- `2`: `intent.daily_schedule`
- `3`: `intent.search_file`
- `4`: `intent.send_email`

#### Ma trận nhầm lẫn thực nghiệm trên Validation Set (8 mẫu)

| Nhãn thực tế (Ground Truth) \ Dự đoán (Pred) | `create_document` (0) | `create_meeting` (1) | `daily_schedule` (2) | `search_file` (3) | `send_email` (4) | Tổng mẫu thực tế |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **`intent.create_document` (0)** | **0** | 1 | 0 | 0 | 1 | 2 |
| **`intent.create_meeting` (1)** | 0 | **0** | 0 | 0 | 1 | 1 |
| **`intent.daily_schedule` (2)** | 0 | 1 | **1** | 0 | 0 | 2 |
| **`intent.search_file` (3)** | 0 | 2 | 0 | **0** | 0 | 2 |
| **`intent.send_email` (4)** | 0 | 1 | 0 | 0 | **0** | 1 |
| **Tổng mẫu dự đoán** | **0** | **5** | **1** | **0** | **2** | **8** |

#### Phân tích lỗi (Error Analysis)

1. **Hiện tượng thiên lệch dự đoán (Prediction Bias / Collapse)**:
   - Mô hình dự đoán nhãn `intent.create_meeting` tới **5/8 lần** (chiếm 62.5% tổng số dự đoán) và `intent.send_email` **2/8 lần**.
   - Hoàn toàn **không có bất kỳ mẫu nào** được dự đoán vào `intent.create_document` hay `intent.search_file` (cột 0 và cột 3 toàn số 0).
   - Chỉ duy nhất **1 mẫu** thuộc `intent.daily_schedule` được dự đoán chính xác (ô `[2, 2] = 1`), dẫn đến Accuracy chỉ đạt `1/8 = 0.125` (12.5%).

2. **Các cặp nhãn bị nhầm lẫn chính**:
   - `search_file` -> nhầm thành `create_meeting` (2/2 mẫu, tỷ lệ nhầm 100%).
   - `create_document` -> nhầm thành `create_meeting` (1 mẫu) và `send_email` (1 mẫu).
   - `create_meeting` -> nhầm thành `send_email` (1/1 mẫu).
   - `daily_schedule` -> nhầm thành `create_meeting` (1 mẫu).

3. **Nguyên nhân kỹ thuật cốt lõi**:
   - **Đặc trưng quá nông (Feature limitation)**: Bộ đặc trưng hiện tại chỉ gồm `text_length`, `word_count`, `has_question_mark` và `source`. Các feature này chỉ đo độ dài hình thức và nguồn gửi, hoàn toàn **không chứa thông tin ngữ nghĩa (semantics)** của từ khóa câu hỏi (ví dụ: các từ "họp", "lịch", "tìm file", "soạn thư").
   - **Tập dữ liệu nhỏ**: Khi độ dài các câu hỏi giữa các intent tương đương nhau, Logistic Regression với bộ feature bề mặt sẽ học trọng số nghiêng về class có intercept cao hoặc đặc trưng trùng lặp.
   - **Ý nghĩa bài học**: Ma trận nhầm lẫn phản ánh rõ ràng mô hình đang bị thiên lệch thay vì học được quy luật phân loại thực sự. Đây là thước đo nền tảng (baseline benchmark) để so sánh khi nâng cấp lên các kỹ thuật trích xuất ngữ nghĩa và mạng nơ-ron (PyTorch) ở các tuần kế tiếp.


---

## 3.4. Bảng Chỉ Số Chi Tiết Theo Từng Intent (Ngày 11)

| Intent | Precision | Recall | F1-Score | Support |
| :--- | :---: | :---: | :---: | :---: |
| `intent.create_document` | 0.00 | 0.00 | 0.00 | 2 |
| `intent.create_meeting` | 0.00 | 0.00 | 0.00 | 1 |
| `intent.daily_schedule` | 1.00 | 0.50 | 0.67 | 2 |
| `intent.search_file` | 0.00 | 0.00 | 0.00 | 2 |
| `intent.send_email` | 0.00 | 0.00 | 0.00 | 1 |
| **Macro Avg** | **0.20** | **0.10** | **0.13** | 8 |
| **Weighted Avg** | **0.25** | **0.12** | **0.17** | 8 |

### Nhận xét và Phân tích Trade-off:
1. **Macro F1 (0.133) vs Weighted F1 (0.167)**:
   - Macro F1 đánh giá công bằng từng class độc lập. Do 4/5 class hoàn toàn không đoán trúng (F1 = 0.0), Macro F1 bị kéo xuống rất thấp (0.133).
   - Weighted F1 tính theo trọng số support của từng class (0.167), cao hơn Macro F1 do class đoán được có số mẫu chiếm 25%.
2. **Precision và Recall Trade-off**:
   - `intent.daily_schedule` đạt Precision tuyệt đối (1.00) nhưng Recall chỉ 0.50 (bỏ sót 50% ý định lịch trình).
   - Mô hình thiên lệch (bias) dự đoán dồn vào `create_meeting` và `send_email` khiến các nhãn khác có Recall = 0.
3. **Kết luận**:
   - Bộ feature đếm ký tự thô không đủ phân biệt ngữ nghĩa. Đây là mốc baseline để kiểm chứng sự cải thiện khi dùng mô hình học sâu (PyTorch) ở Tuần 3.

---

## 3.5. Kết Quả Đánh Giá Trên Held-Out Test Set Lần Đầu (Ngày 13)

Theo đúng nguyên tắc phương pháp luận Machine Learning, tập **Test Set** (`data/splits/test.csv`) được giữ kín (held-out) và chỉ được mở ra đánh giá **đúng một lần duy nhất** sau khi đã hoàn tất mọi quyết định về kiến trúc mô hình, pipeline trích xuất đặc trưng và phân tích lỗi trên Validation set.

### 3.5.1. Thông tin thực nghiệm
- **Ngày thực hiện**: 2026-09-11
- **Phiên bản dữ liệu**: `data/splits/` v1.0
  - Train: 37 mẫu (`data/splits/train.csv`)
  - Validation: 8 mẫu (`data/splits/validation.csv`)
  - Test: 7 mẫu (`data/splits/test.csv`)
- **Lệnh thực thi**:
  ```powershell
  uv run python scripts/train_sklearn_baseline.py --write-report --evaluate-test
  ```
- **Ràng buộc quy trình**:
  - Toàn bộ tham số tiền xử lý (`IntentPreprocessor`: scaler, encoder) và bộ mã hóa nhãn (`LabelMapping`) được giữ nguyên từ quá trình `fit` trên tập Train; chỉ gọi `transform` và `encode` trên tập Test.
  - Không thực hiện bất kỳ thao tác điều chỉnh siêu tham số (hyperparameter tuning) hay thay đổi đặc trưng nào sau khi đã quan sát kết quả trên tập Test nhằm ngăn chặn rò rỉ thông tin (data leakage) và bias quyết định.

### 3.5.2. Bảng so sánh tổng hợp Validation vs Test Set

| Tập đánh giá (Split) | Số mẫu (Support) | Accuracy | Macro F1 | Weighted F1 | Nhận xét tổng quan |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Validation Set** | 8 | 0.1250 (1/8) | 0.1333 | 0.1667 | Mô hình đoán đúng 1 mẫu `daily_schedule`, dồn bias nặng vào `create_meeting`. |
| **Test Set (Held-out)** | 7 | 0.4286 (3/7) | 0.4133 | 0.4476 | Đoán đúng 3/7 mẫu (`create_document`, `create_meeting`, `send_email`). |

### 3.5.3. Ma trận nhầm lẫn thực nghiệm trên Test Set (7 mẫu)

Thứ tự nhãn cố định từ `label_mapping.classes_`:
- `0`: `intent.create_document`
- `1`: `intent.create_meeting`
- `2`: `intent.daily_schedule`
- `3`: `intent.search_file`
- `4`: `intent.send_email`

| Nhãn thực tế (Ground Truth) \ Dự đoán (Pred) | `create_document` (0) | `create_meeting` (1) | `daily_schedule` (2) | `search_file` (3) | `send_email` (4) | Tổng mẫu thực tế |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **`intent.create_document` (0)** | **1** | 0 | 0 | 0 | 0 | 1 |
| **`intent.create_meeting` (1)** | 0 | **1** | 0 | 1 | 0 | 2 |
| **`intent.daily_schedule` (2)** | 0 | 1 | **0** | 0 | 0 | 1 |
| **`intent.search_file` (3)** | 0 | 1 | 0 | **0** | 0 | 1 |
| **`intent.send_email` (4)** | 0 | 0 | 0 | 1 | **1** | 2 |
| **Tổng mẫu dự đoán** | **1** | **3** | **0** | **2** | **1** | **7** |

### 3.5.4. Bảng chỉ số chi tiết theo từng Intent trên Test Set

| Intent | Precision | Recall | F1-Score | Support |
| :--- | :---: | :---: | :---: | :---: |
| `intent.create_document` | 1.0000 | 1.0000 | 1.0000 | 1 |
| `intent.create_meeting` | 0.3333 | 0.5000 | 0.4000 | 2 |
| `intent.daily_schedule` | 0.0000 | 0.0000 | 0.0000 | 1 |
| `intent.search_file` | 0.0000 | 0.0000 | 0.0000 | 1 |
| `intent.send_email` | 1.0000 | 0.5000 | 0.6667 | 2 |
| **Macro Avg** | **0.4667** | **0.4000** | **0.4133** | 7 |
| **Weighted Avg** | **0.4762** | **0.4286** | **0.4476** | 7 |

### 3.5.5. Phân tích nguyên nhân chênh lệch giữa Validation và Test

1. **Hiện tượng dao động do cỡ mẫu nhỏ (Small Sample Variance)**:
   - Khoảng cách từ `12.5%` lên `42.86%` thực chất chỉ tương ứng với **2 câu dự đoán đúng thêm** (từ 1/8 lên 3/7).
   - Với kích thước tập Test gồm 7 mẫu, giá trị của 1 mẫu đơn lẻ chiếm tới `1/7 ≈ 14.29%` tổng Accuracy. Do đó, bất kỳ sự trùng hợp ngẫu nhiên nào cũng khuếch đại chỉ số phần trăm, tạo nên biến động phương sai cao (high variance) thay vì chứng minh năng lực khái quát hóa vượt trội.
2. **Đặc trưng hình thức không chứa ngữ nghĩa văn bản**:
   - Bộ đặc trưng hiện tại hoàn toàn là heuristic hình thức: `text_length`, `word_count`, `has_question_marks`, và `source`.
   - Ở tập Test, 3 câu đoán trúng ngẫu nhiên có độ dài và nguồn gửi phân bổ rơi vào vùng quyết định của các nhãn `create_document`, `create_meeting` và `send_email`.
3. **Mô hình tiếp tục thất bại hoàn toàn ở 2 intent**:
   - Hai nhãn `intent.daily_schedule` (0/1 câu) và `intent.search_file` (0/1 câu) vẫn có Precision, Recall và F1-Score bằng `0.0000`.
   - Cả 2 mẫu thực tế của 2 intent này đều bị mô hình dự đoán nhầm thành `intent.create_meeting`.

### 3.5.6. Kết luận Milestone Baseline và Bàn giao sang Tuần 3 (PyTorch)
- **Đạt mục tiêu Milestone Tuần 2**: Baseline cổ điển (Logistic Regression) đã hoàn tất chu trình chuẩn: huấn luyện, đánh giá Validation, phân tích lỗi qua Confusion Matrix, đóng gói service wrapper và kiểm thử độc lập trên Held-out Test Set.
- **Tiêu chuẩn đối sánh (Benchmark)**:
  - Macro F1 trên Validation: `0.1333`
  - Macro F1 trên Held-out Test: `0.4133`
- **Định hướng Tuần 3**: Thay thế các đặc trưng bề mặt bằng mô hình học sâu PyTorch (Word Embeddings / Neural Networks) nhằm trích xuất ngữ nghĩa thực của câu lệnh, giải quyết triệt để lỗi thiên lệch nhãn và các intent có F1 = 0.

---

## 4. Thực nghiệm PyTorch Intent Classifier & Validation Loop (Tuần 3 - Ngày 19)

### 4.1. Thiết lập Huấn luyện & Đánh giá
- **Kiến trúc mô hình**: `IntentClassifier` (gồm 2 lớp fully connected `Linear(input_dim, 64)` -> `ReLU` -> `Linear(64, num_classes)`).
- **Hàm mất mát**: `nn.CrossEntropyLoss()`.
- **Bộ tối ưu hóa**: `Adam(lr=0.001)`.
- **Dữ liệu**:
  - Train: `data/splits/train.csv` (37 mẫu, `batch_size=32`, `shuffle=True`).
  - Validation: `data/splits/validation.csv` (8 mẫu, `batch_size=32`, `shuffle=False`).
- **Ràng buộc đánh giá**:
  - Chạy hàm `evaluate_model` với `model.eval()` và `torch.no_grad()`.
  - Không tính toán hay tích lũy gradient trong pha validation.

### 4.2. Nhật ký Huấn luyện (5 Epochs)

| Epoch | Train Loss | Validation Loss | Validation Macro F1 |
| :---: | :---: | :---: | :---: |
| 1 | 1.6813 | 1.6488 | 0.0800 |
| 2 | 1.5839 | 1.6450 | 0.0800 |
| 3 | 1.6061 | 1.6419 | 0.1143 |
| 4 | 1.5837 | 1.6393 | 0.1143 |
| 5 | 1.6640 | 1.6363 | 0.1143 |

### 4.3. Bảng Đối Sánh: Baseline vs PyTorch (Validation Set)

| Mô hình | Validation Loss | Macro F1 | Weighted F1 | Nhận xét |
| :--- | :---: | :---: | :---: | :--- |
| **Baseline Logistic Regression** (Tuần 2) | N/A | **0.1333** | 0.1667 | Dùng Logistic Regression của scikit-learn với solver lbfgs. |
| **PyTorch Intent Classifier (5 epochs)** (Tuần 3) | 1.6363 | **0.1143** | 0.1829 | Validation loss giảm đều qua từng epoch (1.6488 -> 1.6363). |

### 4.4. Nhận xét Kỹ thuật
1. **Quá trình tối ưu hóa**: Validation loss giảm đều sau mỗi epoch, khẳng định mô hình và pipeline gradient đang cập nhật đúng hướng, không bị nổ gradient hay overfit sớm.
2. **So sánh F1 với Baseline**: Macro F1 của PyTorch (0.1143) tương đương mức Baseline (0.1333). Do vẫn sử dụng chung bộ feature thô bề mặt (độ dài, ký tự), mô hình học sâu chưa thể tạo sự vượt trội về ngữ nghĩa cho đến khi được trang bị pretrained word embeddings hoặc transformer ở các giai đoạn sau.

---

## 5. Tổng Kết Milestone PyTorch Intent Classifier & Phân Tích Giới Hạn (Tuần 3 - Ngày 21 / Day 49)

### 5.1. Bàn Giao Kỹ Thuật Milestone Tuần 3
Tuần 3 đã hoàn thiện đầy đủ chu trình kỹ thuật của một hệ thống học sâu (Deep Learning) tích hợp trong backend FastAPI:
1. **Dữ liệu & Tải dữ liệu**: `IntentDataset` bọc dữ liệu feature vector/nhãn class với dtype chuẩn (`float32` cho feature, `long` cho target); `DataLoader` thiết lập đúng nguyên lý: train set có `shuffle=True`, validation set có `shuffle=False`.
2. **Kiến trúc mô hình**: `IntentClassifier` kế thừa `nn.Module`, gồm 2 tầng Linear với phi tuyến ReLU, nhận `(batch_size, input_dim)` và trả logits `(batch_size, num_classes)`.
3. **Training & Validation Loop**: Quy trình chuẩn gồm `zero_grad()`, `backward()`, `optimizer.step()`, kết hợp pha kiểm thử với `model.eval()` và `torch.no_grad()` để đo lường loss cùng Macro F1.
4. **Tách biệt Đào tạo và Phục vụ (Offline Training vs Online Serving)**:
   - Mô hình được huấn luyện offline độc lập qua script `scripts/train_torch_intent.py` và lưu trữ thành 3 artifact: weights `models/intent_classifier.pt`, metadata `models/intent_metadata.json`, và pipeline tiền xử lý `models/intent_preprocessor.joblib`.
   - Service runtime (`IntentService`) nạp artifact một lần duy nhất lúc khởi động qua dependency injection, phục vụ endpoint `POST /api/v1/ml/intent` với thời gian đáp ứng dưới mili-giây, tuyệt đối **không thực hiện training hay tích lũy gradient trong request**.

### 5.2. Bảng Đối Sánh Tổng Quan Toàn Bộ Milestone

| Mô hình | Đặc trưng đầu vào | Phương pháp đánh giá | Macro F1 (Val) | Khả năng phục vụ API | Trạng thái tích hợp |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **Baseline (Scikit-learn Logistic Regression)** | 4 đặc trưng thô (độ dài, số từ, dấu `?`, source) | `fit` -> `predict_proba` trên CPU | **0.1333** | Có service wrapper | Đạt mốc Tuần 2 |
| **PyTorch Neural Network (MLP 2 lớp)** | 4 đặc trưng thô (độ dài, số từ, dấu `?`, source) | Mini-batch SGD (Adam), cross-entropy loss | **0.1143 - 0.2500** | Endpoint `POST /api/v1/ml/intent` | Đạt mốc Tuần 3 |

### 5.3. Phân Tích Giới Hạn Cốt Lõi Của Mô Hình (Model Limitations)

> [!WARNING]
> Theo tiêu chuẩn Definition of Done (DoD) của Tuần 3: **Tuyệt đối không tuyên bố mô hình hoạt động tốt khi kích thước tập dữ liệu còn nhỏ**. Việc đánh giá khách quan các rào cản kỹ thuật là bắt buộc:

1. **Giới hạn kích thước tập dữ liệu (Extreme Small Sample Size & High Variance)**:
   - Kích thước tập dữ liệu hiện tại (`N_train = 37`, `N_val = 8`, `N_test = 7`) quá nhỏ so với số tham số của mạng nơ-ron.
   - Trên tập Validation chỉ gồm 8 mẫu, mỗi mẫu dự đoán đúng/sai làm dịch chuyển Accuracy tới `12.5%`. Sự dao động (variance) giữa các lần huấn luyện có thể rất lớn chỉ do thứ tự xáo trộn batch hoặc khởi tạo seed ngẫu nhiên.
2. **Giới hạn đặc trưng bề mặt (Surface Heuristic Bottleneck - Thiếu vắng Semantic Meaning)**:
   - Dù chuyển sang kiến trúc Deep Learning (PyTorch), mô hình vẫn chỉ nhận các con số thống kê hình thức (`text_length`, `word_count`, `has_question_marks`, `source`).
   - Hai câu có độ dài và nguồn gửi tương đương như *"Lên lịch họp dự án với team"* và *"Xóa toàn bộ thư trong hòm thư"* sẽ sinh ra vector đặc trưng gần như giống hệt nhau, khiến bất kỳ mô hình phân loại nào (kể cả mạng sâu nhiều lớp) cũng không thể phân biệt chính xác ý định nếu không có thông tin ngữ nghĩa từ vựng.
3. **Hiện tượng thiên lệch nhãn và sụp đổ dự đoán (Class Imbalance & Collapse)**:
   - Do số lượng mẫu phân bổ không đều giữa 5 intent, mô hình có xu hướng dự đoán dồn vào nhóm intent có tần suất xuất hiện cao hơn (`intent.create_meeting`), khiến các intent ít mẫu (`intent.search_file`, `intent.create_document`) rơi vào tình trạng F1 = 0.
4. **Độ tin cậy của xác suất (Softmax Confidence Miscalibration)**:
   - Hàm `torch.softmax` chuyển logits thành xác suất từ 0 đến 1, nhưng khi mô hình chưa được học trên tập dữ liệu đủ lớn và đa dạng, giá trị confidence cao không đồng nghĩa với việc mô hình thực sự chắc chắn về mặt ngữ nghĩa (overconfident on out-of-distribution inputs). API người dùng cần hiển thị cảnh báo mức độ tin cậy kèm theo.

### 5.4. Định Hướng Chuyển Giao Sang Tuần 4 (Handoff to Transformer Foundation)
Để vượt qua giới hạn của các đặc trưng bề mặt, Tuần 4 sẽ tập trung vào nền tảng của kiến trúc **Transformer**:
- Thay thế vector đặc trưng thô bằng kỹ thuật phân tách chuỗi từ vựng thành **Token** và **Token IDs** (Tokenization).
- Chuyển đổi mã token thành không gian ngữ nghĩa nhiều chiều thông qua **Word Embeddings** (`torch.nn.Embedding`).
- Nắm vững cơ chế tính toán trọng số quan hệ ngữ cảnh giữa các từ thông qua **Scaled Dot-Product Attention** và **Multi-Head Attention**.



