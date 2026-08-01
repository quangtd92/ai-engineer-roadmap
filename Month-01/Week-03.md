# Tháng 1 - Tuần 3: Async, HTTP client, Docker và integration test

## Mục tiêu tuần

Làm service sẵn sàng chạy local ổn định hơn bằng async endpoint, HTTPX timeout, request ID middleware, Docker và integration test.

## Kiến thức cần đạt

- Chọn `async def` khi có I/O chờ đợi; không biến CPU-bound work thành async giả.
- Đặt timeout cho HTTP client và kiểm thử không gọi network thật.
- Đóng gói app qua Docker và kiểm thử API qua ASGI client.

## Tính năng project sẽ bổ sung

`GET /api/v1/status`, `StatusClient`, request ID response header, Dockerfile, Compose và test integration cho health/chat.

## Kế hoạch từng ngày

### Ngày 15 - Async status endpoint

**Mục tiêu cụ thể:** Thêm `GET /api/v1/status` bằng `async def`. **Kết quả cần đạt:** Route trả `{"status":"ready"}`. **Phân bổ thời gian:** 20 phút đọc, 50 phút code, 30 phút kiểm tra. **Nội dung lý thuyết:** event loop và I/O-bound. **Tài liệu cần đọc:** FastAPI Async trong [RESOURCES.md](./RESOURCES.md). **Bài thực hành:** Tạo status router, dùng `await asyncio.sleep(0)` chỉ để minh họa yield. **Thay đổi cần áp dụng vào ai-assistant-platform:** Có endpoint nền cho kiểm tra readiness. **File dự kiến tạo hoặc sửa:** `app/api/routes/status.py`, `app/main.py`. **Lệnh chạy:** `uv run uvicorn app.main:app --reload`. **Kết quả mong đợi:** `/api/v1/status` trả 200. **Cách kiểm tra kết quả:** Gọi route nhiều lần; không thêm blocking `time.sleep`. **Definition of Done:** Có giải thích ngắn trong code vì route async. **Commit message gợi ý:** `feat(api): add async status endpoint`. **Câu hỏi tự kiểm tra:** Async có làm PyTorch inference CPU nhanh hơn không?

### Ngày 16 - HTTPX client với timeout

**Mục tiêu cụ thể:** Viết client async lấy status từ URL cấu hình. **Kết quả cần đạt:** Timeout và lỗi network thành exception mô tả rõ. **Phân bổ thời gian:** 20 phút đọc, 55 phút code, 25 phút test. **Nội dung lý thuyết:** connect/read timeout và client lifecycle. **Tài liệu cần đọc:** HTTPX Async support, Timeouts trong [RESOURCES.md](./RESOURCES.md). **Bài thực hành:** Tạo `StatusClient` nhận `httpx.AsyncClient`; đặt timeout 2 giây. **Thay đổi cần áp dụng vào ai-assistant-platform:** Service có adapter HTTP tách khỏi route. **File dự kiến tạo hoặc sửa:** `app/services/status_client.py`, `tests/unit/test_status_client.py`. **Lệnh chạy:** `uv run pytest tests/unit/test_status_client.py -q`. **Kết quả mong đợi:** Test mock response và timeout pass. **Cách kiểm tra kết quả:** Dùng `MockTransport`, không gọi URL công khai. **Definition of Done:** Không tạo `AsyncClient` mới trong mỗi lần retry. **Commit message gợi ý:** `feat(status): add timeout-aware async HTTP client`. **Câu hỏi tự kiểm tra:** Vì sao timeout mặc định không đủ rõ cho production?

### Ngày 17 - Request ID middleware

**Mục tiêu cụ thể:** Gắn request ID vào response và log. **Kết quả cần đạt:** Mỗi response có header `X-Request-ID`. **Phân bổ thời gian:** 15 phút đọc, 55 phút code, 30 phút kiểm tra. **Nội dung lý thuyết:** correlation ID và middleware order. **Tài liệu cần đọc:** FastAPI Middleware trong [RESOURCES.md](./RESOURCES.md). **Bài thực hành:** Dùng header client gửi hoặc `uuid4`; không log request body. **Thay đổi cần áp dụng vào ai-assistant-platform:** Có trace thủ công tối thiểu cho lỗi API. **File dự kiến tạo hoặc sửa:** `app/core/middleware.py`, `app/core/logging.py`, `app/main.py`. **Lệnh chạy:** `curl -i -H "X-Request-ID: demo-123" http://127.0.0.1:8000/health`. **Kết quả mong đợi:** Response giữ `demo-123`. **Cách kiểm tra kết quả:** Gọi không header và xác nhận server sinh ID mới. **Definition of Done:** ID không chứa payload hoặc secret. **Commit message gợi ý:** `feat(observability): add request ID middleware`. **Câu hỏi tự kiểm tra:** Request ID khác trace ID thế nào?

### Ngày 18 - Dockerfile dùng `uv`

**Mục tiêu cụ thể:** Đóng gói API thành image chạy được. **Kết quả cần đạt:** Container phục vụ health tại cổng 8000. **Phân bổ thời gian:** 20 phút đọc, 55 phút Dockerfile, 25 phút build. **Nội dung lý thuyết:** layer cache, `.dockerignore`, bind `0.0.0.0`. **Tài liệu cần đọc:** uv in Docker và Dockerfile reference trong [RESOURCES.md](./RESOURCES.md). **Bài thực hành:** Copy lockfile trước source, cài dependency rồi chạy uvicorn. **Thay đổi cần áp dụng vào ai-assistant-platform:** Có runtime tái lập được. **File dự kiến tạo hoặc sửa:** `Dockerfile`, `.dockerignore`. **Lệnh chạy:** `docker build -t ai-assistant-platform:dev .`; `docker run --rm -p 8000:8000 ai-assistant-platform:dev`. **Kết quả mong đợi:** `curl http://localhost:8000/health` trả 200. **Cách kiểm tra kết quả:** Image không copy `.env`, `.venv` hay `.git`. **Definition of Done:** Dockerfile không hard-code secret. **Commit message gợi ý:** `chore(docker): add uv-based application image`. **Câu hỏi tự kiểm tra:** Vì sao copy source trước dependency làm build chậm hơn?

### Ngày 19 - Docker Compose local

**Mục tiêu cụ thể:** Chạy app bằng một compose command. **Kết quả cần đạt:** Service `api` build và map cổng local. **Phân bổ thời gian:** 15 phút đọc, 50 phút cấu hình, 30 phút chạy thử. **Nội dung lý thuyết:** service, port mapping và environment file. **Tài liệu cần đọc:** Docker Compose trong [RESOURCES.md](./RESOURCES.md). **Bài thực hành:** Tạo `docker-compose.yml` chỉ cho API; tham chiếu `.env` tùy chọn, không commit `.env`. **Thay đổi cần áp dụng vào ai-assistant-platform:** Quy trình local nhất quán cho tuần 4. **File dự kiến tạo hoặc sửa:** `docker-compose.yml`, `README.md`. **Lệnh chạy:** `docker compose up --build`. **Kết quả mong đợi:** Log Uvicorn và health trả 200. **Cách kiểm tra kết quả:** `docker compose down` dừng service sạch. **Definition of Done:** Không thêm PostgreSQL, Redis hay Qdrant trước tháng tương ứng. **Commit message gợi ý:** `chore(docker): add local API compose service`. **Câu hỏi tự kiểm tra:** Khi nào `--build` là cần thiết?

### Ngày 20 - Milestone: integration test API

**Mục tiêu cụ thể:** Kiểm thử health, status, chat qua ASGI. **Kết quả cần đạt:** Test không cần server đang chạy. **Phân bổ thời gian:** 15 phút đọc, 70 phút test, 25 phút sửa lỗi, 10 phút ghi chú. **Nội dung lý thuyết:** unit test so với integration test. **Tài liệu cần đọc:** FastAPI Testing trong [RESOURCES.md](./RESOURCES.md). **Bài thực hành:** Dùng `httpx.ASGITransport`, test header request ID và error 400/422. **Thay đổi cần áp dụng vào ai-assistant-platform:** API contract được bảo vệ trước refactor. **File dự kiến tạo hoặc sửa:** `tests/integration/test_health_api.py`, `tests/integration/test_chat_api.py`. **Lệnh chạy:** `uv run pytest tests/integration -q`. **Kết quả mong đợi:** Toàn bộ integration test pass. **Cách kiểm tra kết quả:** Tắt Uvicorn rồi chạy test; test vẫn pass. **Definition of Done:** Không dùng sleep hoặc network thật trong test. **Commit message gợi ý:** `test(api): add integration coverage for core routes`. **Câu hỏi tự kiểm tra:** Integration test nào không thay thế được unit test?

### Ngày 21 - Review, refactor và tài liệu local

**Mục tiêu cụ thể:** Chốt quy trình local trước PyTorch. **Kết quả cần đạt:** README có hai cách chạy và command kiểm tra. **Phân bổ thời gian:** 25 phút review, 35 phút README, 30 phút kiểm tra, 10 phút nghỉ bù. **Nội dung lý thuyết:** Tài liệu vận hành là một phần của sản phẩm. **Tài liệu cần đọc:** Docker Compose docs trong [RESOURCES.md](./RESOURCES.md). **Bài thực hành:** Viết phần prerequisites, `uv run` và `docker compose`; xóa debug không cần thiết. **Thay đổi cần áp dụng vào ai-assistant-platform:** Người khác có thể chạy service local. **File dự kiến tạo hoặc sửa:** `README.md`, Dockerfile, compose, test liên quan. **Lệnh chạy:** `uv run pytest`; `uv run ruff check .`; `docker compose up --build`. **Kết quả mong đợi:** Ba kiểm tra hoàn tất theo thứ tự. **Cách kiểm tra kết quả:** Làm theo README từ terminal mới. **Definition of Done:** README không hứa hẹn LLM/RAG chưa tồn tại. **Commit message gợi ý:** `docs(project): document local and Docker workflows`. **Câu hỏi tự kiểm tra:** Lỗi nào cần được ghi vào troubleshooting?

## Milestone cuối tuần

API có async status, timeout-aware HTTP client, request ID, Docker runtime và integration test chạy không cần server ngoài.

## Review checklist

- [ ] HTTPX test không gọi network thật.
- [ ] Response có `X-Request-ID`.
- [ ] `docker compose up --build` phục vụ health.
- [ ] Test, lint và README phản ánh hành vi thật.

## Definition of Done

Project khởi chạy và kiểm thử được bằng `uv` lẫn Docker mà không thêm hạ tầng ngoài phạm vi.

## Những lỗi thường gặp

- Dùng `time.sleep()` trong async route.
- Không đặt timeout cho HTTP client.
- Chạy Uvicorn chỉ bind `127.0.0.1` trong container.

## Tài liệu tham khảo chính thức

Xem nhóm Tuần 3 trong [RESOURCES.md](./RESOURCES.md).
