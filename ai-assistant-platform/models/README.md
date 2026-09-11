# Thư Mục Quản Lý Artifacts Mô Hình (Model Artifacts Registry)

Thư mục này lưu trữ các file artifact của mô hình Machine Learning được huấn luyện trong `ai-assistant-platform`. Các artifact được đóng gói sau khi huấn luyện để các service (như `IntentBaselineService`) hoặc API router có thể load và phục vụ suy luận (inference).

---

## 1. Danh sách Artifacts Hiện Có

### `sklearn_intent_baseline.joblib`

- **Phiên bản (model_version)**: `sklearn_intent_v1`
- **Bài toán**: Phân loại ý định người dùng (Multiclass Intent Classification - 5 nhãn)
- **Thuật toán cốt lõi**: `LogisticRegression(max_iter=1000, random_state=42)` từ thư viện `scikit-learn`
- **Script sinh artifact**: [scripts/train_sklearn_baseline.py](file:///e:/repos/cilel1/ai-assistant-platform/scripts/train_sklearn_baseline.py)
- **Kích thước file**: ~3.7 KB

---

## 2. Cấu Trúc Đóng Gói (Artifact Schema)

File artifact được lưu dưới dạng một **Python `dict`** bằng thư viện `joblib`. Cấu trúc các key bên trong bao gồm:

| Khóa (Key) | Kiểu dữ liệu (Type) | Mô tả chi tiết |
| :--- | :--- | :--- |
| `"preprocessor"` | `IntentPreprocessor` | Đối tượng tiền xử lý đã `fit` trên tập train, gồm `StandardScaler` (cho 3 đặc trưng số) và `OneHotEncoder` (cho trường `source`). |
| `"model"` | `LogisticRegression` | Mô hình hồi quy logistic đã huấn luyện trên tập đặc trưng train. |
| `"label_mapping"` | `LabelMapping` | Đối tượng chuyển đổi 2 chiều giữa nhãn chuỗi (string intent) và nhãn số nguyên (`classes_` gồm 5 intent theo thứ tự alphabet). |
| `"model_version"` | `str` | Chuỗi định danh phiên bản: `"sklearn_intent_v1"`. |

> **Lưu ý lập trình**: Do artifact lưu dưới dạng `dict`, cần truy xuất phần tử theo cú pháp index `artifact["preprocessor"]` thay vì truy cập thuộc tính `artifact.preprocessor`.

---

## 3. Cách Sử Dụng Trong Ứng Dụng

### Cách 1: Thông qua Service Wrapper (Khuyến nghị)

Sử dụng trực tiếp [IntentBaselineService](file:///e:/repos/cilel1/ai-assistant-platform/src/ai_assistant_platform/services/intent_baseline_service.py) để đảm bảo tính bao gói và trả về schema chuẩn `PredictionResponse`:

```python
from ai_assistant_platform.services.intent_baseline_service import IntentBaselineService

# Khởi tạo service (load artifact một lần duy nhất vào bộ nhớ)
service = IntentBaselineService(artifact_path="models/sklearn_intent_baseline.joblib")

# Thực hiện dự đoán
response = service.predict("lên lịch họp dự án chiều nay")

print(response.intent)  # Tên intent dự đoán
print(response.confidence)  # Độ tin cậy (predict_proba)
print(response.model_version)  # "sklearn_intent_v1"
```

### Cách 2: Tự load trực tiếp qua `joblib`

```python
from pathlib import Path
import joblib
import pandas as pd

artifact = joblib.load("models/sklearn_intent_baseline.joblib")
preprocessor = artifact["preprocessor"]
model = artifact["model"]
label_mapping = artifact["label_mapping"]

raw_df = pd.DataFrame({"text": ["kiểm tra lịch làm việc"], "source": ["web_ui"]})
features = preprocessor.transform(raw_df)
pred_idx = model.predict(features)[0]
intent_name = label_mapping.classes_[pred_idx]
```

---

## 4. Đặc Trưng Đầu Vào (Feature Pipeline)

Preprocessor biến đổi mỗi văn bản đầu vào thành một vector đặc trưng số (numerical feature vector) kích thước 1D gồm:
1. `text_length`: Độ dài chuỗi ký tự (đã chuẩn hóa qua `StandardScaler`).
2. `word_count`: Số lượng từ trong câu (đã chuẩn hóa qua `StandardScaler`).
3. `has_question_marks`: Cờ nhị phân biểu thị câu có chứa ký tự `?` hay không (đã chuẩn hóa qua `StandardScaler`).
4. `source`: Vector One-Hot 3 chiều tương ứng với nguồn gửi (`app_desktop`, `phone`, `web_ui`).

---

## 5. Hiệu Năng Tham Chiếu (Baseline Benchmark)

Các chỉ số được ghi nhận chi tiết tại [docs/ml-evaluation-report.md](file:///e:/repos/cilel1/ai-assistant-platform/docs/ml-evaluation-report.md):

| Tập đánh giá | Số mẫu | Accuracy | Macro F1 | Weighted F1 |
| :--- | :---: | :---: | :---: | :---: |
| **Validation Set** | 8 | 0.1250 | 0.1333 | 0.1667 |
| **Held-out Test Set** | 7 | 0.4286 | 0.4133 | 0.4476 |

---

## 6. Lệnh Tái Tạo và Kiểm Thử

Để huấn luyện lại và cập nhật file artifact:

```powershell
# Chạy huấn luyện, lưu artifact và xuất report validation/test
uv run python scripts/train_sklearn_baseline.py --write-report --evaluate-test

# Chạy unit test kiểm tra tính toàn vẹn của service wrapper
uv run python -m pytest tests/unit/test_intent_baseline_service.py -v
```

---

## 7. Quy Tắc Bảo Mật & Quản Trị

- File `.joblib` sử dụng cơ chế serialize của Python (tương tự pickle). Tuyệt đối **không** load các file artifact từ nguồn không đáng tin cậy bên ngoài.
- Khi dung lượng mô hình lớn hơn (ví dụ mô hình PyTorch / Transformer ở các tuần tiếp theo), xem xét sử dụng Git LFS hoặc lưu trữ tại Object Storage (S3, GCS) thay vì commit file nhị phân lớn trực tiếp vào repository.
