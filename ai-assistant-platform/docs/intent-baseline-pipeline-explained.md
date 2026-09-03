# Kiến Trúc & Luồng Hoạt Động Của Intent Baseline Pipeline (scikit-learn)

Tài liệu này giải thích chi tiết mục đích thiết kế, ý nghĩa của các thành phần dữ liệu, lý do xây dựng mô hình cơ sở (baseline) và toàn bộ luồng hoạt động từ đầu đến cuối của mô hình phân loại ý định (`Intent Classification`) trong `ai-assistant-platform`.

---

## 1. Bức Tranh Tổng Thể: Bài Toán Cần Giải Quyết

Trong hệ thống trợ lý ảo (`AI Assistant Platform`), người dùng gửi các câu lệnh/yêu cầu bằng văn bản tự nhiên. Hệ thống cần tự động xác định **ý định** (`intent`) để điều hướng xử lý logic tiếp theo:

- `"Cho tôi xem các cuộc họp trong tuần này"` -> `intent.daily_schedule`
- `"Lên lịch họp tổng kết quý vào thứ Sáu"` -> `intent.create_meeting`
- `"Soạn email cho team marketing"` -> `intent.send_email`
- `"Có file 'kế hoạch marketing' ở đâu?"` -> `intent.search_file`
- `"Khởi tạo tài liệu kế hoạch phát triển quý 4"` -> `intent.create_document`

Đây là bài toán **Học có giám sát (Supervised Learning) - Phân loại đa lớp (Multi-class Classification)**.

---

## 2. Bản Chất Dữ Liệu: Ma Trận Đặc Trưng `X` và Nhãn Mục Tiêu `y`

File dữ liệu gốc (`data/splits/train.csv`) gồm các cột:
`id`, `text`, `intent`, `source`, `created_at`.

### 2.1. Tại sao `y` là `intent` mà không phải field khác?
- **`y` (Target / Ground Truth)**: Là kết quả cuối cùng mà bài toán kinh doanh cần dự đoán. Hệ thống cần biết **ý định của người dùng**, do đó nhãn mục tiêu bắt buộc phải là `intent`.
- Các trường khác trong file không được chọn làm `y` vì:
  - `id`: Mã số định danh ngẫu nhiên của dòng dữ liệu trong database, hoàn toàn vô nghĩa đối với suy luận.
  - `created_at`: Thời điểm ghi nhận bản ghi log, không phải nghiệp vụ cần dự đoán.
  - `source`: Nguồn gửi tin nhắn (`web_ui`, `app_desktop`, `phone`) là thông tin hệ thống đã biết sẵn ngay khi nhận request từ client, không cần mô hình phải đoán.

### 2.2. `X` không phải là tất cả các field
Bộ tiền xử lý `IntentPreprocessor` không lấy toàn bộ DataFrame, mà chọn lọc và biến đổi:
- **Bỏ qua hoàn toàn**: `id`, `created_at`, và chính cột `intent` (để tránh rò rỉ đáp án).
- **Chỉ trích xuất từ 2 cột**:
  - `text`: Tính 3 đặc trưng số (`text_lengths`, `word_counts`, `has_question_marks`).
  - `source`: Mã hóa one-hot qua `OneHotEncoder`.
- **Kết quả**: Ma trận số thực 2D `X` đại diện cho các đặc trưng đầu vào (Input Features).

---

### 2.3. Ý Nghĩa Của Việc Chuyển Text Thành Đặc Trưng Hình Thức (`text_lengths`, `word_counts`, `has_question_marks`)

1. **Về mặt kỹ thuật ML**:
   - Thuật toán `LogisticRegression` (và hầu hết các mô hình học máy toán học) chỉ có thể nhân ma trận và tính toán trên các số thực (`float`/`int`). Thuật toán không thể nhận trực tiếp một chuỗi văn bản (string) tiếng Việt. Bắt buộc phải có bước chuyển đổi từ chuỗi sang vector số.

2. **Giả thuyết ban đầu (Heuristic Features)**:
   - `has_question_marks`: Phân biệt câu hỏi tra cứu thông tin (`daily_schedule`, `search_file` - thường có dấu `?`) với câu mệnh lệnh yêu cầu hành động (`create_meeting`, `create_document` - thường không có dấu `?`).
   - `text_lengths` & `word_counts`: Giả định câu yêu cầu soạn tài liệu/email thường dài và chi tiết hơn các câu lệnh tra cứu ngắn.

3. **Hạn chế thực tế**:
   - Ngữ nghĩa của Intent nằm ở **từ khóa** ("họp", "mail", "lịch", "file"), chứ không nằm ở độ dài hay số từ.
   - Hai câu có cấu trúc tương tự nhau:
     - *"Lên lịch họp chiều nay"* (`create_meeting`): 5 từ, 22 ký tự, không có dấu `?`.
     - *"Soạn email gửi cho sếp"* (`send_email`): 5 từ, 21 ký tự, không có dấu `?`.
   - Về mặt số học trong vector `X`, hai câu trên gần như y hệt nhau, khiến mô hình không thể phân biệt và phải đoán mò. Kết quả thực nghiệm trên tập validation chỉ đạt Accuracy **12.5%** và bị thiên lệch nặng.

---

## 3. Tại Sao Mô Hình Baseline "Tệ Nhất" Lại KHÔNG Được Bỏ Qua?

Trong kỹ nghệ AI sản phẩm (AI Engineering), việc xây dựng một Baseline Model dù rất ngây thơ (naive) là bước đi bắt buộc vì 3 nguyên tắc cốt lõi:

### 3.1. Thông toàn bộ đường ống kỹ thuật (End-to-End Pipeline Integrity)
Trước khi quan tâm mô hình thông minh hay ngốc, phải đảm bảo toàn bộ hệ thống phần mềm chạy được từ đầu đến cuối mà không bị gãy vỡ:
- Đọc file CSV, xử lý missing value và duplicate.
- Bộ tiền xử lý `fit` trên tập train và `transform` độc lập trên tập validation để tránh rò rỉ dữ liệu (Data Leakage).
- Quá trình huấn luyện (`fit`) và suy luận (`predict`) diễn ra bình thường.
- Đóng gói (`joblib.dump`) thành công toàn bộ bundle (`preprocessor`, `model`, `label_mapping`).
- File artifact có thể nạp lên Service/API backend để phục vụ request.

Nếu nhảy thẳng vào mô hình Deep Learning/Transformer phức tạp, khi xảy ra lỗi bạn sẽ không thể biết lỗi do hạ tầng dữ liệu hay do kiến trúc mạng nơ-ron gây ra.

### 3.2. Tạo mốc đo lường chuẩn (Benchmark Ground Truth)
Làm sao chứng minh được một mô hình Transformer (tốn kém GPU, độ trễ cao, phức tạp) thực sự xứng đáng để đầu tư?
- **Baseline (mô hình cơ sở thô sơ)**: Accuracy **12.5%**, độ trễ **1 ms**, tiêu tốn **0 đồng** tài nguyên.
- **Mô hình cải tiến (TF-IDF / Word Embeddings / Transformer)**: Accuracy nhảy vọt lên **85% - 95%**.

Nếu không có Baseline, bạn không có bằng chứng khoa học và định lượng nào để chứng minh mô hình mới đang tốt lên hay tệ đi.

### 3.3. Nguyên tắc phát triển MVP (Minimum Viable Product)
- Đội ngũ Backend và Frontend cần một mô hình chạy được ngay trong vòng **30 phút** để tích hợp giao diện, dựng API endpoint, hoàn thiện luồng người dùng.
- Kỹ sư ML sau đó có thể an tâm tối ưu thuật toán mà không làm nghẽn tiến độ của toàn bộ dự án.

---

## 4. Chi Tiết Luồng Hoạt Động 5 Bước Của Pipeline

```
[ train.csv / validation.csv ]
              │
              ▼
   ┌───────────────────────┐
   │  IntentPreprocessor   │ ──> Trích xuất [text_len, word_count, has_?] + One-Hot(source) ──> X (Features Matrix)
   └───────────────────────┘
              │
   ┌───────────────────────┐
   │     LabelMapping      │ ──> Ánh xạ nhãn chữ ('create_meeting', ...) thành số [0..4]     ──> y (Target Vector)
   └───────────────────────┘
              │
              ▼
   ┌───────────────────────┐
   │  LogisticRegression   │ ──> model.fit(X_train, y_train): Học trọng số liên kết giữa X và y
   └───────────────────────┘
              │
              ▼
   ┌───────────────────────┐
   │ Model Evaluation & CM │ ──> model.predict(X_val) -> Confusion Matrix & Error Analysis
   └───────────────────────┘
              │
              ▼
   ┌───────────────────────┐
   │    Packaging (.joblib)│ ──> joblib.dump({"preprocessor", "model", "label_mapping"}, path)
   └───────────────────────┘
```

### Bước 1: Nạp và Phân Tách Dữ Liệu
Dữ liệu được nạp từ `data/splits/train.csv` và `data/splits/validation.csv`. Hai tập này hoàn toàn tách biệt.

### Bước 2: Trích Xuất Đặc Trưng (`IntentPreprocessor`)
- `fit(df_train)`: Học thống kê phân phối (trung bình, độ lệch chuẩn của độ dài câu; danh sách các giá trị `source`).
- `transform(df_train)` & `transform(df_validation)`: Áp dụng các tham số đã học để biến đổi dữ liệu thành ma trận số `X_train` và `X_validation`.

### Bước 3: Mã Hóa Nhãn (`LabelMapping`)
- Cố định thứ tự nhãn theo bảng chữ cái:
  - `0`: `intent.create_document`
  - `1`: `intent.create_meeting`
  - `2`: `intent.daily_schedule`
  - `3`: `intent.search_file`
  - `4`: `intent.send_email`
- Chuyển cột `intent` thành vector nhãn số nguyên `y_train` và `y_validation`.

### Bước 4: Huấn Luyện Mô Hình (`LogisticRegression`)
- Lệnh: `model.fit(X_train, y_train)`
- Bản chất: Thuật toán tìm nghiệm tối ưu cho hàm mất mát (Log-Loss) để xác định các trọng số (weights) và hệ số tự do (bias) liên hệ giữa `X` và xác suất của từng nhãn `y`.

### Bước 5: Đánh Giá Lỗi & Đóng Gói
1. **Dự đoán**: Gọi `model.predict(X_validation)` sinh ra `y_val_pred`.
2. **Ma trận nhầm lẫn (Confusion Matrix)**: Dùng `calculate_confusion_matrix(y_validation, y_val_pred)` để chỉ ra cụ thể class nào đang bị nhầm sang class nào (tìm ra nguyên nhân thiên lệch).
3. **Đóng gói Artifact**: Gom cả 3 đối tượng (`intent_preprocessor`, `model`, `label_mapping`) vào dictionary và lưu xuống ổ đĩa tại `models/sklearn_intent_baseline.joblib`.

---

## 5. Kết Luận & Bước Tiếp Theo

Mô hình baseline đã hoàn thành xuất sắc vai trò: **Xác thực toàn bộ đường ống xử lý dữ liệu, huấn luyện, đánh giá và đóng gói.**

Ở các giai đoạn tiếp theo (Tuần 3 & 4), khi thay thế bộ đặc trưng bề mặt bằng các kỹ thuật biểu diễn ngữ nghĩa (TF-IDF, Word2Vec, hoặc mạng nơ-ron PyTorch / Transformer), đường ống kỹ thuật này vẫn giữ nguyên, chỉ có chất lượng của bộ trích xuất đặc trưng và mô hình được nâng cấp vượt bậc.
