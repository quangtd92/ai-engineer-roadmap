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
*(Sẽ được cập nhật từ Ngày 9 - Ngày 11)*

| Model Version | Accuracy | Macro F1 | Weighted F1 | Ghi chú / Lỗi chính quan sát được |
| :--- | :--- | :--- | :--- | :--- |
| *Baseline Logistic Regression* | *Chưa chạy* | *Chưa chạy* | *Chưa chạy* | *Chờ thực nghiệm Ngày 9* |

### 3.3. Confusion Matrix & Error Analysis
*(Sẽ được bổ sung ma trận nhầm lẫn 5x5 ở Ngày 10 để phân tích các cặp intent hay bị dự đoán nhầm)*
