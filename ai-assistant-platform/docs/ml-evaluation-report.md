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
| *Baseline Logistic Regression* | `0.125` (1/8) | *Chờ Ngày 11* | *Chờ Ngày 11* | Model bị lệch (bias) nặng về `create_meeting` và `send_email`; chỉ dùng 4 feature bề mặt nên thiếu ngữ nghĩa văn bản. |

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
