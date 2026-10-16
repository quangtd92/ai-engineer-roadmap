# AI Assistant Platform

Service FastAPI backend phục vụ ứng dụng AI Assistant Platform với đầy đủ middleware quản lý Request ID, xử lý lỗi chuẩn hóa, async status & health check endpoint, và hỗ trợ chạy containerized với Docker.

---

## 📋 Prerequisites (Yêu cầu môi trường)

Để chạy dự án ở môi trường local, bạn cần chuẩn bị:

- **Python**: `>= 3.12`
- **uv**: Package manager cực nhanh dành cho Python (`pip install uv` hoặc cài theo [trang chủ uv](https://docs.astral.sh/uv/))
- **Docker & Docker Compose**: (Tùy chọn) Để chạy service trong môi trường containerized.

---

## 🚀 Local Development (Chạy ứng dụng Local)

### 1. Khởi tạo môi trường & cài đặt phụ thuộc

```powershell
uv sync
```

### 2. Chạy ứng dụng

#### Cách 1: Sử dụng `uv` (Khuyên dùng khi phát triển)

- **Chạy trực tiếp với `uvicorn`**:
  ```powershell
  uv run uvicorn ai_assistant_platform.main:app --reload --port=8001
  ```
- **Hoặc qua module entrypoint**:
  ```powershell
  uv run python -m ai_assistant_platform.main
  ```

Ứng dụng sẽ lắng nghe tại: `http://localhost:8001`

#### Cách 2: Sử dụng `Docker Compose`

- **Khởi chạy container**:
  ```bash
  docker compose up --build -d
  ```
- **Dừng container**:
  ```bash
  docker compose down
  ```

---

## 🧪 Testing & Code Quality (Kiểm thử & Linter)

Chạy bộ kiểm thử tự động và kiểm tra chất lượng mã nguồn:

- **Chạy toàn bộ Integration & Unit Tests**:
  ```powershell
  uv run pytest
  ```
- **Kiểm tra Linting**:
  ```powershell
  uv run ruff check .
  ```
- **Tự động sửa lỗi Linting**:
  ```powershell
  uv run ruff check --fix .
  ```
- **Định dạng code (Format)**:
  ```powershell
  uv run ruff format .
  ```

---

## 📖 API Documentation & Endpoints

### Documentation
- **Swagger UI**: [http://localhost:8001/docs](http://localhost:8001/docs)
- **OpenAPI Schema**: [http://localhost:8001/openapi.json](http://localhost:8001/openapi.json)

### Danh sách Endpoint chính

| Method | Endpoint | Mô tả |
| :--- | :--- | :--- |
| `GET` | `/api/v1/health` | Health check endpoint trả về trạng thái service & tên môi trường |
| `GET` | `/api/v1/status` | Async status endpoint kiểm tra khả năng phục vụ |
| `POST` | `/api/v1/chat` | Echo/process endpoint gửi tin nhắn tới assistant |
| `POST` | `/api/v1/inference/score` | Chấm điểm deterministic PyTorch toy model từ vector số thực |
| `POST` | `/api/v1/ml/intent` | Dự đoán ý định người dùng (Intent Classification) bằng PyTorch Neural Network |

### 🧠 Huấn Luyện Mô Hình ML (Machine Learning Training Pipeline)

Dự án tách biệt hoàn toàn giữa quá trình **Huấn luyện Offline** và **Phục vụ Trực tuyến (Online Serving)**:

1. **Huấn luyện mô hình PyTorch Intent Classifier**:
   ```powershell
   # Huấn luyện 5 epochs và lưu model artifact (.pt, metadata .json, preprocessor .joblib)
   uv run python scripts/train_torch_intent.py --epochs 5 --save-model
   ```
   Artifacts sinh ra trong thư mục `models/`:
   - `models/intent_classifier.pt`: Trọng số mạng nơ-ron PyTorch (`state_dict`).
   - `models/intent_metadata.json`: Cấu hình kiến trúc, số chiều input/hidden/classes và nhãn phân loại.
   - `models/intent_preprocessor.joblib`: Pipeline tiền xử lý (`IntentPreprocessor` đã fit trên tập train).

2. **Huấn luyện mô hình Scikit-learn Baseline (Tham chiếu)**:
   ```powershell
   uv run python scripts/train_sklearn_baseline.py --write-report --evaluate-test
   ```

### Ví dụ Lệnh `curl` kiểm tra

1. **Health Check**:
   ```powershell
   curl -X GET "http://localhost:8001/api/v1/health"
   ```

2. **Async Status Check**:
   ```powershell
   curl -X GET "http://localhost:8001/api/v1/status"
   ```

3. **Gửi tin nhắn Chat**:
   ```powershell
   curl -X POST "http://localhost:8001/api/v1/chat" `
     -H "Content-Type: application/json" `
     -d "{\"content\": \"Xin chào AI Assistant\"}"
   ```

4. **PyTorch Intent Prediction Endpoint**:
   ```powershell
   curl -X POST "http://localhost:8001/api/v1/ml/intent" `
     -H "Content-Type: application/json" `
     -d "{\"text\": \"Tôi muốn kiểm tra lịch làm việc hôm nay\", \"source\": \"web_ui\"}"
   ```
   *Kết quả mẫu*:
   ```json
   {
     "intent": "intent.daily_schedule",
     "confidence": 0.4215,
     "model_version": "torch_intent_v1"
   }
   ```

5. **PyTorch Toy Model Inference** (Vector số thực)
   ```powershell
   curl -X POST "http://localhost:8001/api/v1/inference/score" `
     -H "Content-Type: application/json" `
     -d "{\"values\": [1.0, 2.0]}"
   ```

---

## 🛠️ Troubleshooting (Xử lý lỗi thường gặp)

1. **Lỗi chiếm dụng cổng `8001` (`Address already in use`)**:
   - Kiểm tra process đang dùng cổng 8001 hoặc đổi cổng trong `.env` (`APP_PORT=8002`) hoặc khi chạy Uvicorn.
2. **Khác biệt IP giữa Local và Docker**:
   - Khi chạy local ngoài máy thật, Uvicorn mặc định bind vào `127.0.0.1`.
   - Trong Docker container, Uvicorn được cấu hình bind vào `0.0.0.0` để có thể nhận request từ bên ngoài container.
3. **Thiếu file cấu hình môi trường `.env`**:
   - Sao chép từ mẫu `.env.example`:
     ```powershell
     cp .env.example .env
     ```
4. **Lỗi `Artifact not found at models/...` khi gọi endpoint intent**:
   - Chạy lệnh huấn luyện để sinh artifact trước khi khởi động server:
     ```powershell
     uv run python scripts/train_torch_intent.py --epochs 5 --save-model
     ```

---

## 🧪 Quy trình chạy và Lệnh Smoke Test đầy đủ (Docker & Local)

### **Bước 1: Huấn luyện và chuẩn bị Artifact**
```powershell
uv run python scripts/train_torch_intent.py --epochs 5 --save-model
```

### **Bước 2: Build và khởi động Container**
```powershell
# Chạy tại thư mục ai-assistant-platform
docker compose up --build -d
```

### **Bước 3: Health Check**
```powershell
curl -X GET "http://localhost:8001/api/v1/health"
```
*Kết quả mong đợi*: `HTTP 200 OK`, `{"status":"ok","environment":"development"}`

### **Bước 4: Status Check**
```powershell
curl -X GET "http://localhost:8001/api/v1/status"
```
*Kết quả mong đợi*: `HTTP 200 OK`, `{"message":"Service is healthy and ready to process requests."}`

### **Bước 5: Intent Classification Smoke Test (PyTorch)**
```powershell
curl -X POST "http://localhost:8001/api/v1/ml/intent" `
     -H "Content-Type: application/json" `
     -d "{\"text\": \"Tạo một cuộc họp vào 2h chiều\", \"source\": \"web_ui\"}"
```
*Kết quả mong đợi*: `HTTP 200 OK`, `{"intent":"intent.create_meeting","confidence":0.35,"model_version":"torch_intent_v1"}`

### **Bước 6: Chat Endpoint**
```powershell
curl -X POST "http://localhost:8001/api/v1/chat" `
     -H "Content-Type: application/json" `
     -d "{\"content\": \"Xin chào AI Assistant\"}"
```
*Kết quả mong đợi*: `HTTP 200 OK`, `{"content":"Xin chào AI Assistant","request_id":"..."}`

---

## 🤖 Nguyên Tắc Thiết Kế: Offline Training vs Online Serving

> [!IMPORTANT]
> **Separation of Concerns trong MLOps / AI Engineering**:
> - **Huấn luyện (Offline Training)**: Tốn tài nguyên tính toán (backpropagation, autograd, data shuffle) và diễn ra theo batch định kỳ thông qua `scripts/train_torch_intent.py`.
> - **Phục vụ (Online Serving)**: Endpoint FastAPI `/api/v1/ml/intent` tải trọng số tĩnh (`models/intent_classifier.pt`) và tiền xử lý (`models/intent_preprocessor.joblib`) qua Singleton / Dependency Injection. Ở mỗi request, hệ thống đặt chế độ `model.eval()`, bọc khối `torch.no_grad()`, và suy luận trong vài mili-giây.
> - **Tuyệt đối không chạy training hay cập nhật gradient bên trong request lifecycle của API**.

Chi tiết thực nghiệm và phân tích giới hạn mô hình xem tại: [docs/ml-evaluation-report.md](docs/ml-evaluation-report.md).
