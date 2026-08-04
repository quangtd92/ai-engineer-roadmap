# Tháng 03 — Tuần 01: Responses API, streaming và độ tin cậy

## Mục tiêu tuần

Tạo đường đi LLM đầu tiên theo kiến trúc `route → ChatService → LLMClient`, có config an toàn, error mapping, timeout/retry, streaming SSE và telemetry. Chỉ sau khi contract fake chạy ổn mới thử API thật.

## Kiến thức và feature sẽ bổ sung

- Responses API, instructions/input roles, model configuration, request timeout và retry có giới hạn.
- Async streaming, SSE và khác biệt giữa first-token latency với tổng latency.
- `src/ai_assistant_platform/llm/openai_client.py`, `src/ai_assistant_platform/services/chat_service.py`, route chat/stream và `src/ai_assistant_platform/observability/llm_metrics.py`.

## Kế hoạch từng ngày

### Ngày 01 — Contract LLM và cấu hình không lộ secret

- **Mục tiêu:** thiết kế interface trước khi cài SDK.
- **Kết quả cần đạt:** `LLMClient` protocol và `LLMSettings` đọc `OPENAI_API_KEY` từ environment, không in giá trị key.
- **Thời lượng (90 phút):** 20 phút xem Responses API trong [README tháng](./README.md#tài-liệu-tham-khảo-đã-chọn), 45 phút code, 15 phút test, 10 phút ghi chú.
- **Lý thuyết:** dependency inversion và config boundary.
- **Tài liệu:** đọc [Responses API reference](https://platform.openai.com/docs/api-reference/responses), phần request input và response object.
- **Bài thực hành:** tạo fake client trả `LLMResult(text, request_id, usage)`.
- **Tích hợp project:** route hiện có vẫn dùng fake qua dependency.
- **File:** `src/ai_assistant_platform/core/config.py`, `src/ai_assistant_platform/llm/contracts.py`, `.env.example`, `tests/unit/test_config.py`.
- **Lệnh:** `uv run pytest tests/unit/test_config.py -q`.
- **Kết quả mong đợi:** thiếu key không làm import package thất bại.
- **Kiểm tra:** assert error chỉ nêu tên biến, không chứa giá trị fixture.
- **DoD:** `.env` không được tạo/commit.
- **Commit:** `feat(llm): add provider contract and safe settings`.
- **Tự kiểm tra:** Vì sao key không nên được validate lúc module import? Fake client giúp test điều gì?

### Ngày 02 — Responses API adapter tối thiểu

- **Mục tiêu:** map request nội bộ sang một lời gọi Responses API.
- **Kết quả cần đạt:** adapter gọi `responses.create` và chuyển output text/usage sang `LLMResult`.
- **Thời lượng (100 phút):** 25 phút đọc reference, 50 phút code với mock SDK, 15 phút test, 10 phút ghi chú.
- **Lý thuyết:** adapter cô lập vendor SDK, instructions khác user input.
- **Tài liệu:** đọc [Responses API reference](https://platform.openai.com/docs/api-reference/responses), phần create response và usage.
- **Bài thực hành:** mock client SDK thay vì gọi network.
- **Tích hợp project:** `ChatService.reply()` nhận `ChatRequest` cũ.
- **File:** `src/ai_assistant_platform/llm/openai_client.py`, `src/ai_assistant_platform/services/chat_service.py`, `tests/unit/test_openai_client.py`.
- **Lệnh:** `uv run pytest tests/unit/test_openai_client.py -q`.
- **Kết quả mong đợi:** model, instructions và input được truyền đúng.
- **Kiểm tra:** mock output không có usage vẫn trả `usage=None`.
- **DoD:** route chưa import SDK trực tiếp.
- **Commit:** `feat(llm): add responses api adapter`.
- **Tự kiểm tra:** Adapter bảo vệ phần nào khi đổi provider? Vì sao không giả định usage luôn tồn tại?

### Ngày 03 — Error taxonomy và timeout

- **Mục tiêu:** biến lỗi upstream thành lỗi API dự đoán được.
- **Kết quả cần đạt:** timeout, auth/configuration và lỗi upstream map sang domain exception có HTTP status an toàn.
- **Thời lượng (95 phút):** 20 phút đọc, 45 phút code, 20 phút test, 10 phút ghi chú.
- **Lý thuyết:** timeout là giới hạn tài nguyên, không phải retry signal mặc định.
- **Tài liệu:** xem [FastAPI error handling](https://fastapi.tiangolo.com/tutorial/handling-errors/), tập trung vào HTTP exception handler.
- **Bài thực hành:** fake client ném `TimeoutError`/provider exception.
- **Tích hợp project:** exception handler trả `503` hoặc `504`, không trả raw provider body.
- **File:** `src/ai_assistant_platform/llm/errors.py`, `src/ai_assistant_platform/api/error_handlers.py`, `tests/integration/test_chat_errors.py`.
- **Lệnh:** `uv run pytest tests/integration/test_chat_errors.py -q`.
- **Kết quả mong đợi:** timeout trả mã và `code` ổn định.
- **Kiểm tra:** response không chứa API key hoặc stack trace.
- **DoD:** timeout được cấu hình qua settings.
- **Commit:** `feat(chat): map llm failures safely`.
- **Tự kiểm tra:** Lỗi nào không nên retry? Vì sao lỗi auth không phải 500?

### Ngày 04 — Chat thật với smoke test tùy chọn

- **Mục tiêu:** nối `POST /api/v1/chat` với adapter.
- **Kết quả cần đạt:** request hợp lệ trả text LLM khi environment có key; fake vẫn làm integration test offline.
- **Thời lượng (100 phút):** 15 phút đọc, 50 phút route/dependency, 20 phút test, 15 phút smoke test tùy chọn.
- **Lý thuyết:** dependency override và integration test không tốn token.
- **Tài liệu:** đọc [FastAPI dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/), phần dependency override trong test.
- **Bài thực hành:** bổ sung `model` allowlist trong settings, inject service.
- **Tích hợp project:** thay mock cứng bằng dependency provider.
- **File:** `src/ai_assistant_platform/api/routes/chat.py`, `src/ai_assistant_platform/api/dependencies.py`, `tests/integration/test_chat_api.py`.
- **Lệnh:** `uv run pytest tests/integration/test_chat_api.py -q`; tùy chọn `uv run uvicorn ai_assistant_platform.main:app --reload`.
- **Kết quả mong đợi:** offline test 200 với fake; smoke test thật trả một câu.
- **Kiểm tra:** chạy không key phải trả lỗi cấu hình có hướng dẫn, không crash.
- **DoD:** model không nhận từ body người dùng.
- **Commit:** `feat(chat): connect route to llm service`.
- **Tự kiểm tra:** Vì sao model là server configuration? Test nào được phép gọi API thật?

### Ngày 05 — Retry bounded và backoff có chọn lọc

- **Mục tiêu:** retry transient failure đúng một nơi.
- **Kết quả cần đạt:** retry tối đa 2 lần cho lỗi tạm thời; không retry validation/auth/timeout theo mặc định.
- **Thời lượng (90 phút):** 20 phút lý thuyết idempotency/backoff, 45 phút code, 15 phút test, 10 phút ghi chú.
- **Lý thuyết:** retry phải bị chặn bởi loại lỗi và số lần thử.
- **Tài liệu:** xem [OpenAI API error codes](https://platform.openai.com/docs/guides/error-codes), phần lỗi có thể retry.
- **Bài thực hành:** inject sleeper để test không cần chờ thật.
- **Tích hợp project:** `RetryPolicy` nằm trong adapter.
- **File:** `src/ai_assistant_platform/llm/retry.py`, `src/ai_assistant_platform/llm/openai_client.py`, `tests/unit/test_retry.py`.
- **Lệnh:** `uv run pytest tests/unit/test_retry.py -q`.
- **Kết quả mong đợi:** transient fake thành công ở attempt hai; permanent fake chỉ gọi một lần.
- **Kiểm tra:** assert attempts và delay schedule.
- **DoD:** không có `while True`.
- **Commit:** `feat(llm): add bounded transient retry`.
- **Tự kiểm tra:** Retry có thể làm tăng chi phí ra sao? Vì sao cần phân loại lỗi?

### Ngày 06 — Streaming SSE

- **Mục tiêu:** stream text mà không ghép toàn bộ response trước khi gửi.
- **Kết quả cần đạt:** `POST /api/v1/chat/stream` phát event `token`, rồi `done` hoặc `error`.
- **Thời lượng (110 phút):** 25 phút đọc StreamingResponse, 55 phút async generator, 20 phút test, 10 phút ghi chú.
- **Lý thuyết:** SSE framing, cancellation và completion event.
- **Tài liệu:** đọc [FastAPI StreamingResponse](https://fastapi.tiangolo.com/advanced/custom-response/#streamingresponse) và [Responses streaming events](https://platform.openai.com/docs/api-reference/responses-streaming).
- **Bài thực hành:** fake async stream phát ba chunk.
- **Tích hợp project:** route dùng `StreamingResponse`, không đổi endpoint thường.
- **File:** `src/ai_assistant_platform/llm/streaming.py`, `src/ai_assistant_platform/api/routes/chat.py`, `tests/integration/test_chat_stream.py`.
- **Lệnh:** `uv run pytest tests/integration/test_chat_stream.py -q`.
- **Kết quả mong đợi:** body có thứ tự `event: token` và `event: done`.
- **Kiểm tra:** fake ném lỗi giữa stream tạo duy nhất event error rồi đóng.
- **DoD:** không log text prompt/response đầy đủ.
- **Commit:** `feat(chat): add bounded sse streaming`.
- **Tự kiểm tra:** Vì sao `done` khác với kết nối đóng? Client xử lý lỗi giữa stream thế nào?

### Ngày 07 — Milestone telemetry LLM

- **Mục tiêu:** đo được vận hành cơ bản của chat/stream.
- **Kết quả cần đạt:** structured log có request id, model, latency ms, usage nếu có và error code.
- **Thời lượng (105 phút):** 20 phút thiết kế field, 45 phút instrumentation, 25 phút chạy test, 15 phút review.
- **Lý thuyết:** usage/cost awareness; không suy diễn giá tiền nếu thiếu bảng giá.
- **Tài liệu:** xem [Responses API reference](https://platform.openai.com/docs/api-reference/responses), phần `usage`, để phân biệt token usage với billing.
- **Bài thực hành:** dùng clock fake để test latency.
- **Tích hợp project:** cả success/failure của `ChatService` ghi event chuẩn.
- **File:** `src/ai_assistant_platform/observability/llm_metrics.py`, `src/ai_assistant_platform/services/chat_service.py`, `tests/unit/test_llm_metrics.py`, `README.md`.
- **Lệnh:** `uv run pytest tests/unit/test_llm_metrics.py -q`; `uv run ruff check .`.
- **Kết quả mong đợi:** test chứng minh log không chứa key/prompt.
- **Kiểm tra:** request thành công và timeout đều có request id.
- **DoD:** có bảng field telemetry trong README project.
- **Commit:** `feat(observability): log llm latency usage and errors`.
- **Tự kiểm tra:** Latency nào cần đo cho streaming? Tại sao usage không phải lúc nào cũng là cost?

## Milestone, review và DoD

- **Milestone:** offline test chứng minh chat thường/stream/error mapping; smoke test thật là tùy chọn.
- **Review checklist:** [ ] adapter không lộ vào route; [ ] retry ≤2 và có test; [ ] SSE có done/error; [ ] log không chứa secret/prompt đầy đủ.
- **Definition of Done:** chat service có thể thay fake bằng OpenAI adapter qua dependency và đo được outcome.
- **Lỗi thường gặp:** đặt key trong source, retry mọi exception, buffer hết stream, cho client chọn model.
- **Tùy chọn (≤30 phút):** đo time-to-first-token trong fake stream.
- **Tài liệu:** xem 4 nguồn OpenAI/FastAPI/Pydantic trong [README tháng](./README.md#tài-liệu-tham-khảo-đã-chọn).
