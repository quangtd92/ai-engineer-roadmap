# Month 02 Handoff & Technical Baseline

Tài liệu này tổng kết toàn bộ kiến trúc nền tảng đạt được sau **Month 01** và xác định hợp đồng kỹ thuật (contracts), baseline cùng các điểm chuyển giao cho **Month 02** (Deep Learning & Neural Networks).

---

## 1. Tổng kết Kiến trúc Nền tảng (Month 01 Baseline)

Trong Month 01, dự án `ai-assistant-platform` đã xây dựng hoàn chỉnh khung ứng dụng backend chuẩn production:

1. **Python & Package Management**: Sử dụng Python `3.12+` với công cụ quản lý package siêu tốc `uv`.
2. **FastAPI Web Framework**:
   - Kiến trúc module hóa rõ ràng: `api/routes`, `api/schemas`, `core/`, `domain/`, `services/`.
   - Dependency Injection với `@lru_cache` cho `Settings` và `InferenceService`.
   - Middleware quản lý `X-Request-ID` cho phép tracing request xuyên suốt.
   - Hệ thống xử lý lỗi chuẩn hóa (`PlatformError`, `InvalidMessageError`, `NotFoundError`, `ExternalServiceError`, `LLMProviderError`, `RequestValidationError`) trả về schema lỗi thống nhất (`code`, `detail`).
3. **Async & Network I/O**:
   - Endpoint bất đồng bộ `/api/v1/status`.
   - `StatusClient` dựa trên `httpx.AsyncClient` có cấu hình timeout rõ ràng và bọc lỗi HTTP/Network thành domain exceptions.
4. **Containerization**:
   - `Dockerfile` tối ưu nhiều layer, non-root user (nếu cần), bỏ qua các file thừa với `.dockerignore`.
   - `docker-compose.yml` phục vụ triển khai và smoke test đồng nhất.
5. **Testing & Quality Assurance**:
   - 100% tests tự động (28 unit & integration tests) với `pytest`.
   - Tuân thủ linting và formatting nghiêm ngặt với `ruff`.

---

## 2. PyTorch Foundation & Toy Model Baseline

Trong Tuần 4 của Month 01, các khái niệm cốt lõi của PyTorch đã được tích hợp vào hệ thống:

### Các khái niệm đã làm chủ
- **Tensor Structure**:
  - `shape`: Kích thước các chiều tensor (ví dụ: `[batch_size, input_dim]`).
  - `dtype`: Kiểu dữ liệu số học (chuẩn hóa `torch.float32` cho neural network inputs).
  - `device`: Vị trí tensor (CPU hoặc GPU CUDA).
- **Inference Mode & Gradient Isolation**:
  - `model.eval()`: Chuyển các layer đặc thù (Dropout, BatchNorm) sang chế độ đánh giá.
  - `with torch.no_grad()`: Tắt tính toán autograd engine, giảm tải RAM và tăng tốc độ xử lý.
- **Dataset & DataLoader Mechanism**:
  - Kế thừa `torch.utils.data.Dataset` (`__len__`, `__getitem__`).
  - Sử dụng `DataLoader` để chia batch dữ liệu và shuffle tự động.

### ⚠️ Giới hạn rõ ràng của Toy Model (Disclaimer)
- Endpoint `/api/v1/inference/score` hiện sử dụng **Toy Linear Model** (`nn.Linear(2, 1)`) với seed cố định (`torch.manual_seed(2)`).
- **Mục đích**: Thiết lập và kiểm thử toàn bộ luồng tích hợp PyTorch vào API service (validation đầu vào, forward pass, tensor-to-scalar serialization, error handling).
- **Giới hạn**: Model này **chưa có trọng số học từ dữ liệu thật**, kết quả đầu ra là điểm tính toán mẫu (deterministic score baseline), **không** được sử dụng như một dự đoán nghiệp vụ hoàn chỉnh.

---

## 3. Hợp đồng Dữ liệu & Kế hoạch Kỹ thuật cho Month 02

Month 02 sẽ tập trung vào **Neural Networks, Data Processing, Loss Functions, Optimizers và Training Loops**. Dưới đây là các contract cần tuân thủ khi mở rộng:

### 3.1. Data Preprocessing & Tensor Contract
- **Input Validation**: Mọi dữ liệu dạng số đầu vào phải được validate thông qua Pydantic schema (chặn `NaN`, `Inf`, kiểm tra kích thước danh sách) trước khi đưa vào PyTorch Tensor.
- **Dtype Standardization**: Tất cả vector đặc trưng đầu vào phải ép kiểu tường minh sang `torch.float32`.
- **Batch Dimension**:
  - Trong training loop: Luôn xử lý theo batch dạng `(batch_size, num_features)`.
  - Trong inference API: Giữ batch dimension linh hoạt (hỗ trợ cả single input `(1, num_features)` lẫn mini-batch `(N, num_features)`).

### 3.2. DataLoader & Batching Strategy
- **Training Phase**:
  - Sử dụng `DataLoader(dataset, batch_size=..., shuffle=True, drop_last=False)`.
  - Tách tập dữ liệu thành Train / Validation / Test sets.
- **Inference Phase**:
  - Tuyệt đối không load lại model trong từng request. Model được khởi tạo duy nhất 1 lần trong `InferenceService` (singleton via dependency injection).
  - Luôn bọc inference trong `with torch.no_grad():` và chuyển kết quả sang kiểu dữ liệu Python gốc (ví dụ: `.item()` hoặc `.tolist()`).

### 3.3. Memory & Resource Management
- Tránh rò rỉ bộ nhớ (GPU/CPU memory leak): Không lưu trữ các tensor còn đính kèm computation graph (`requires_grad=True`) vào session, cache hoặc response context.
- Log chi tiết thời gian inference (latency) và metadata mà không log raw payloads nhạy cảm.

---

## 4. Checklist Sẵn sàng Bàn giao (Handoff Checklist)

- [x] Linter pass 100%: `uv run ruff check .`
- [x] Test suite pass 100%: `uv run pytest` (28/28 tests passed)
- [x] Không còn file tạm, code nháp hoặc `TODO` tồn đọng.
- [x] File `.env` được bảo mật (nằm trong `.gitignore`, có sẵn `.env.example`).
- [x] Cấu hình Docker Compose sẵn sàng cho smoke testing.
- [x] Tài liệu hướng dẫn sử dụng và handoff được cập nhật đầy đủ.
