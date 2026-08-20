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

4. **PyTorch Toy Model Inference** (Sử dụng curl)
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

---

## 🧪 Quy trình chạy và Lệnh Smoke Test đầy đủ

### **Bước 1: Build và khởi động Container**
```powershell
# Chạy tại thư mục ai-assistant-platform
docker compose up --build -d
```

### **Bước 2: Health Check**
```powershell
curl -X GET "http://localhost:8001/api/v1/health"
```
*Kết quả mong đợi*: `HTTP 200 OK`, `{"status":"ok","environment":"development"}`

### **Bước 3: Status Check**
```powershell
curl -X GET "http://localhost:8001/api/v1/status"
```
*Kết quả mong đợi*: `HTTP 200 OK`, `{"message":"Service is healthy and ready to process requests."}`

### **Bước 4: Chat Endpoint**
```powershell
curl -X POST "http://localhost:8001/api/v1/chat" `
     -H "Content-Type: application/json" `
     -d "{\"content\": \"Xin chào AI Assistant\"}"
```
*Kết quả mong đợi*: `HTTP 200 OK`, `{"content":"Xin chào AI Assistant","request_id":"..."}`

### **Bước 5: Toy Model Inference**
```powershell
curl -X POST "http://localhost:8001/api/v1/inference/score" `
     -H "Content-Type: application/json" `
     -d "{\"values\": [1.0, 2.0]}"
```
*Kết quả mong đợi*: `HTTP 200 OK`, `{"score": <giá trị float>}`


