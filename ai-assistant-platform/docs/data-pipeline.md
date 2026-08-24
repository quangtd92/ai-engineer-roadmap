# Data Pipeline & Feature Engineering (Month 02)

Tài liệu này ghi nhận kiến trúc pipeline xử lý dữ liệu và thiết kế ma trận đặc trưng (feature matrix) cho project `ai-assistant-platform`.

---

## 1. Tổng quan Kiến trúc Data Pipeline

Dữ liệu thô (raw data) dạng văn bản không thể đưa trực tiếp vào các mô hình Machine Learning hoặc Neural Network dạng số. Pipeline dữ liệu đảm nhiệm chuyển đổi dữ liệu từ dạng bảng/văn bản sang ma trận số (`ndarray`) với schema chặt chẽ.

```mermaid
flowchart LR
    A[data/raw/intent_samples.csv] --> B[pandas Inspection & Cleaning]
    B --> C[Feature Extraction & Encoding]
    C --> D[2D NumPy Feature Matrix X]
    D --> E[scikit-learn Baseline / PyTorch Tensor]
```

---

## 2. Nền tảng NumPy: Shape, Dtype và Vectorization

### 2.1 Ma trận Đặc trưng `X` (2D Array)
Trong Machine Learning chuẩn, ma trận dữ liệu đầu vào $X$ luôn có dạng 2 chiều (2D array):
- **`shape` = `(N, D)`**:
  - `N` (trục `axis=0`): Số lượng mẫu quan sát (samples / rows).
  - `D` (trục `axis=1`): Số lượng đặc trưng (features / columns).
- **`ndim` = 2**: Số chiều của mảng.
- **`nbytes`**: Dung lượng bộ nhớ thực tế của mảng liên tục (contiguous memory buffer).

### 2.2 Vai trò của `dtype`
- **Numeric Dtype (`float32`, `int32`, `float64`)**: Cung cấp cấu trúc mảng đồng nhất (homogeneous), lưu trữ các số nhị phân liên tiếp trong RAM, cho phép tận dụng SIMD (Single Instruction, Multiple Data) của CPU/GPU.
- **Tại sao tránh `object` dtype?**: Kiểu `object` trong NumPy thực chất là mảng chứa các con trỏ trỏ tới Python object nằm rải rác trong bộ nhớ (pointer chasing). Điều này làm mất khả năng vector hóa phần cứng, gây overhead bộ nhớ lớn và khiến các thư viện như scikit-learn hoặc PyTorch báo lỗi hoặc chạy chậm gấp hàng chục lần.

### 2.3 Vectorization và Trục (Axis)
- **Vectorization**: Thay vì dùng vòng lặp Python (`for` loop) chậm chạp qua từng phần tử, vectorization thực hiện phép toán đồng thời trên toàn bộ mảng ở tầng mã máy C/Fortran.
- **Khái niệm `axis` trong tính toán thống kê**:
  - `axis=0` (Dọc theo các hàng): Thống kê đặc trưng trên toàn bộ dataset (ví dụ: `np.mean(X, axis=0)` trả về vector 1D kích thước `(D,)` là giá trị trung bình của từng cột feature).
  - `axis=1` (Ngang qua các cột): Thống kê trên từng dòng quan sát (ví dụ: tổng điểm của từng sample).
- **Boolean Masking**: Lọc dữ liệu tốc độ cao không qua vòng lặp, ví dụ `is_question = X[:, 2] == 1.0` tạo ra mảng boolean mask dùng để trích xuất hoặc đếm `np.sum(is_question)`.

---

## 3. Đặc trưng Văn bản Cơ bản (Baseline Text Features)

Ở giai đoạn Ngày 30 (Tuần 1 - Ngày 2), hệ thống trích xuất 3 đặc trưng số học cơ bản từ cột `text` trước khi sử dụng các phương pháp phức tạp hơn như TF-IDF hay Embedding:

| Index | Tên Feature | Mô tả | Kiểu Dữ liệu |
|---|---|---|---|
| 0 | `text_length` | Độ dài của câu tính theo số ký tự (`len(text)`) | `float32` |
| 1 | `word_count` | Số lượng từ trong câu (`len(text.split())`) | `float32` |
| 2 | `has_question_mark` | Cờ nhị phân (1 nếu có `?`, 0 nếu không) | `float32` |

Script thực hiện: [`scripts/numpy_text_features.py`](file:///d:/Du-an/AI-Engineer-Roadmap/ai-assistant-platform/scripts/numpy_text_features.py)

---

## 4. Tự kiểm tra Kiến thức (Self-Check Q&A)

### Q1: Vì sao model cần input dạng ma trận numeric?
> **Trả lời:** Các thuật toán ML (hồi quy, cây quyết định, SVM, Neural Network) đều dựa trên các phép toán đại số tuyến tính (nhân ma trận, tính khoảng cách khoảng không gian vector, gradient descent). Dữ liệu phi cấu trúc như text hoặc categorical cần được biểu diễn dưới dạng số (`float32`/`int32`) để thực hiện các phép tính toán học này.

### Q2: `shape[0]` và `shape[1]` biểu diễn gì?
> **Trả lời:** Trong ma trận 2D $X$:
> - `shape[0]` biểu diễn số lượng mẫu dữ liệu (samples / observations / data points).
> - `shape[1]` biểu diễn số lượng đặc trưng đo lường (features / dimensions).

### Q3: Dtype `object` gây khó khăn gì?
> **Trả lời:** 
> 1. Mất tính tối ưu hóa SIMD / Cache locality do bộ nhớ bị phân mảnh (mảng chứa con trỏ trỏ tới Python object).
> 2. Không tương thích trực tiếp với các framework C++/CUDA như PyTorch C-extension, scikit-learn Cython backend, gây lỗi type mismatch.
> 3. Tốn RAM và làm chậm quá trình huấn luyện/suy luận.
