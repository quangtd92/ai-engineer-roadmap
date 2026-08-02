# Tháng 1 - Tuần 2: FastAPI, Pydantic và API structure

## Mục tiêu tuần

Đưa logic chat của tuần 1 vào FastAPI, thêm Pydantic schema, config environment, dependency injection và error response nhất quán.

## Kiến thức cần đạt

- Request body và `response_model` trong FastAPI.
- Pydantic validation ở HTTP boundary, không trộn với domain object.
- Router, dependency và exception handler có phạm vi rõ ràng.

## Tính năng project sẽ bổ sung

FastAPI app có `/health`, `POST /api/v1/chat`, OpenAPI docs và config từ `.env`.

## Kế hoạch từng ngày

### Ngày 8 - FastAPI app và health endpoint

**Mục tiêu cụ thể:** Tạo ứng dụng FastAPI có `GET /health`. **Kết quả cần đạt:** Uvicorn trả JSON `{"status":"ok"}`. **Phân bổ thời gian:** 20 phút đọc, 55 phút code, 25 phút kiểm tra. **Nội dung lý thuyết:** app instance, route decorator, status code. **Tài liệu cần đọc:** FastAPI Tutorial và Request Body trong [RESOURCES.md](./RESOURCES.md). **Bài thực hành:** Cài `fastapi` và `uvicorn[standard]`; tạo `src/ai_assistant_platform/main.py`, `src/ai_assistant_platform/api/routes/health.py`. **Thay đổi cần áp dụng vào ai-assistant-platform:** Có API entry point đầu tiên. **File dự kiến tạo hoặc sửa:** `pyproject.toml`, `uv.lock`, `src/ai_assistant_platform/main.py`, `src/ai_assistant_platform/api/routes/health.py`. **Lệnh chạy:** `uv run uvicorn ai_assistant_platform.main:app --reload`. **Kết quả mong đợi:** `GET http://127.0.0.1:8000/health` trả HTTP 200. **Cách kiểm tra kết quả:** Mở `/docs` và gọi health từ Swagger UI. **Definition of Done:** Router health được include từ `main.py`. **Commit message gợi ý:** `feat(api): add FastAPI health endpoint`. **Câu hỏi tự kiểm tra:** Vì sao health không gọi dependency ngoài mạng?

### Ngày 9 - Pydantic schema cho chat

**Mục tiêu cụ thể:** Định nghĩa `ChatRequest` và `ChatResponse`. **Kết quả cần đạt:** Content rỗng hoặc toàn khoảng trắng bị từ chối với HTTP 422 khi schema được dùng. **Phân bổ thời gian:** 20 phút đọc, 55 phút code, 25 phút thử request. **Nội dung lý thuyết:** field constraint, validation error và serialization. **Tài liệu cần đọc:** Pydantic Models và FastAPI Request Body trong [RESOURCES.md](./RESOURCES.md). **Bài thực hành:** Tạo model có `content` dài 1-2.000 ký tự và `reply`. **Thay đổi cần áp dụng vào ai-assistant-platform:** Chuẩn hóa contract chat trước khi nối service. **File dự kiến tạo hoặc sửa:** `src/ai_assistant_platform/api/schemas/chat.py`, `src/ai_assistant_platform/api/schemas/__init__.py`. **Lệnh chạy:** `uv run python -c "from ai_assistant_platform.api.schemas.chat import ChatRequest; print(ChatRequest(content='Xin chào'))"`. **Kết quả mong đợi:** In model hợp lệ; input trống báo `ValidationError`. **Cách kiểm tra kết quả:** Thử `content` là ba khoảng trắng. **Definition of Done:** Không trả domain dataclass trực tiếp ra HTTP. **Commit message gợi ý:** `feat(chat): add Pydantic request and response schemas`. **Câu hỏi tự kiểm tra:** HTTP 422 khác gì domain error của tuần 1?

### Ngày 10 - Chat router dùng service hiện có

**Mục tiêu cụ thể:** Tạo `POST /api/v1/chat` gọi `build_mock_reply`. **Kết quả cần đạt:** Request hợp lệ trả `ChatResponse` với reply. **Phân bổ thời gian:** 15 phút thiết kế, 60 phút code, 25 phút kiểm tra. **Nội dung lý thuyết:** Router là adapter; service không biết HTTP. **Tài liệu cần đọc:** FastAPI Bigger Applications trong [RESOURCES.md](./RESOURCES.md). **Bài thực hành:** Tạo router, đổi `ChatRequest` thành `ChatMessage` trong route. **Thay đổi cần áp dụng vào ai-assistant-platform:** Mock chat thành API có version prefix. **File dự kiến tạo hoặc sửa:** `src/ai_assistant_platform/api/routes/chat.py`, `src/ai_assistant_platform/main.py`, `src/ai_assistant_platform/services/chat_service.py`. **Lệnh chạy:** `curl -X POST http://127.0.0.1:8000/api/v1/chat -H "Content-Type: application/json" -d '{"content":"Xin chào"}'`. **Kết quả mong đợi:** HTTP 200 và JSON chứa `reply`. **Cách kiểm tra kết quả:** Gọi bằng Swagger UI và xác nhận OpenAPI hiển thị schema. **Definition of Done:** Route chỉ điều phối schema và service. **Commit message gợi ý:** `feat(chat): expose mock reply through API`. **Câu hỏi tự kiểm tra:** Vì sao không đặt business logic trong router?

### Ngày 11 - Config và environment variables

**Mục tiêu cụ thể:** Đọc `APP_NAME`, `APP_ENV` từ environment. **Kết quả cần đạt:** Health trả tên app và environment không chứa secret. **Phân bổ thời gian:** 20 phút đọc, 50 phút code, 30 phút kiểm tra. **Nội dung lý thuyết:** twelve-factor config và `.env.example`. **Tài liệu cần đọc:** pydantic-settings trong [RESOURCES.md](./RESOURCES.md). **Bài thực hành:** Cài `pydantic-settings`, tạo `Settings`, `.env.example`, `.gitignore` nếu thiếu. **Thay đổi cần áp dụng vào ai-assistant-platform:** Config không hard-code trong route. **File dự kiến tạo hoặc sửa:** `src/ai_assistant_platform/core/config.py`, `.env.example`, `.gitignore`, `src/ai_assistant_platform/api/routes/health.py`. **Lệnh chạy:** `APP_ENV=development uv run uvicorn ai_assistant_platform.main:app --reload`. **Kết quả mong đợi:** Health thể hiện `development`. **Cách kiểm tra kết quả:** Không tạo hoặc commit `.env` chứa API key thật. **Definition of Done:** Biến bắt buộc có default an toàn hoặc lỗi mô tả rõ. **Commit message gợi ý:** `feat(config): load application settings from environment`. **Câu hỏi tự kiểm tra:** Vì sao `.env.example` không chứa giá trị thật?

### Ngày 12 - Dependency injection và metadata

**Mục tiêu cụ thể:** Cấp `Settings` cho router qua dependency. **Kết quả cần đạt:** Không có global config rải rác trong handler. **Phân bổ thời gian:** 20 phút đọc, 50 phút code, 30 phút kiểm tra. **Nội dung lý thuyết:** dependency cache và testability. **Tài liệu cần đọc:** FastAPI Dependencies trong [RESOURCES.md](./RESOURCES.md). **Bài thực hành:** Tạo `get_settings`; thêm title, version, tags cho OpenAPI. **Thay đổi cần áp dụng vào ai-assistant-platform:** Health dependency rõ ràng, docs dễ quét. **File dự kiến tạo hoặc sửa:** `src/ai_assistant_platform/core/config.py`, `src/ai_assistant_platform/api/dependencies.py`, `src/ai_assistant_platform/main.py`, `src/ai_assistant_platform/api/routes/health.py`. **Lệnh chạy:** `uv run uvicorn ai_assistant_platform.main:app --reload`; mở `/docs`. **Kết quả mong đợi:** Docs hiển thị metadata và health vẫn 200. **Cách kiểm tra kết quả:** Override dependency trong một test nhỏ hoặc in settings giả. **Definition of Done:** Route không gọi trực tiếp constructor Settings. **Commit message gợi ý:** `refactor(api): inject settings into health route`. **Câu hỏi tự kiểm tra:** Dependency injection hỗ trợ test thế nào?

### Ngày 13 - Milestone: API error handling

**Mục tiêu cụ thể:** Ánh xạ `InvalidMessageError` thành JSON error có HTTP 400. **Kết quả cần đạt:** Validation schema và domain error có response khác nhau. **Phân bổ thời gian:** 15 phút đọc, 65 phút code, 25 phút test, 15 phút ghi chú. **Nội dung lý thuyết:** exception handler tập trung và không lộ stack trace. **Tài liệu cần đọc:** FastAPI Handling Errors trong [RESOURCES.md](./RESOURCES.md). **Bài thực hành:** Thêm handler, test request schema hợp lệ nhưng service từ chối. **Thay đổi cần áp dụng vào ai-assistant-platform:** Error contract có `code` và `detail`. **File dự kiến tạo hoặc sửa:** `src/ai_assistant_platform/main.py`, `src/ai_assistant_platform/core/errors.py`, `tests/integration/test_chat_api.py`. **Lệnh chạy:** `uv run pytest tests/integration/test_chat_api.py -q`. **Kết quả mong đợi:** Test HTTP 200, 400 và 422 pass. **Cách kiểm tra kết quả:** Không trả exception class hoặc trace trong body. **Definition of Done:** Chỉ domain error đã định nghĩa mới được map 400. **Commit message gợi ý:** `feat(api): add chat domain error handler`. **Câu hỏi tự kiểm tra:** Khi nào nên trả 400 thay vì 422?

### Ngày 14 - Review và OpenAPI check

**Mục tiêu cụ thể:** Kiểm tra contract tuần 2 trước khi thêm async và Docker. **Kết quả cần đạt:** Test, lint và `/openapi.json` nhất quán. **Phân bổ thời gian:** 25 phút review, 40 phút sửa, 25 phút kiểm tra, 10 phút nghỉ bù. **Nội dung lý thuyết:** API contract là đầu vào cho client và integration test. **Tài liệu cần đọc:** FastAPI Response Model trong [RESOURCES.md](./RESOURCES.md). **Bài thực hành:** Rà title, status code, response model, error mẫu; cập nhật README project. **Thay đổi cần áp dụng vào ai-assistant-platform:** Tài liệu local phản ánh endpoint thật. **File dự kiến tạo hoặc sửa:** `README.md`, `src/ai_assistant_platform/main.py`, test liên quan. **Lệnh chạy:** `uv run ruff check .`; `uv run pytest`; `curl http://127.0.0.1:8000/openapi.json`. **Kết quả mong đợi:** Không lỗi lint/test; JSON OpenAPI có ba route. **Cách kiểm tra kết quả:** Đối chiếu đường dẫn docs với curl của ngày 8 và 10. **Definition of Done:** Không còn endpoint thử nghiệm không có schema. **Commit message gợi ý:** `docs(api): review OpenAPI contract for week two`. **Câu hỏi tự kiểm tra:** Client có thể suy ra gì từ `response_model`?

## Milestone cuối tuần

FastAPI service trả health và mock chat qua API versioned, config từ environment và trả domain error có contract rõ ràng.

## Review checklist

- [ ] `/docs` và `/openapi.json` mở được.
- [ ] Chat hợp lệ: 200; schema sai: 422; domain error: 400.
- [ ] `.env.example` không chứa secret.
- [ ] `uv run pytest` và `uv run ruff check .` pass.

## Definition of Done

API tuần 2 có boundary schema rõ, service tuần 1 còn testable không cần FastAPI.

## Những lỗi thường gặp

- Đọc `.env` trực tiếp trong từng route.
- Bắt `Exception` chung và biến mọi lỗi thành 400.
- Bỏ `response_model` khiến contract trôi theo implementation.

## Tài liệu tham khảo chính thức

Xem nhóm Tuần 2 trong [RESOURCES.md](./RESOURCES.md).
