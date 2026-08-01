# Tháng 03 — LLM Engineering, Structured Output, Tool Calling và MCP

## Mục tiêu tháng

Biến `ai-assistant-platform` từ API có câu trả lời giả lập thành một dịch vụ LLM có thể kiểm thử: gọi Responses API, stream SSE, trả Structured Output đã được Pydantic xác thực, gọi hai tool chỉ-đọc theo ngân sách và cung cấp một MCP server tối thiểu. Tháng này không xây RAG hoặc agent; đó là đầu vào cho Tháng 04 và Tháng 05.

## Prerequisite và điểm xuất phát

Người học đã hoàn thành nền Python/FastAPI, Pydantic, async cơ bản, test, Docker và khái niệm token/Transformer ở Tháng 01–02. Giả định project đã có `app/main.py`, route `POST /api/v1/chat` mock, config từ `.env.example`, logging, `tests/unit` và `tests/integration`. Nếu các đầu ra này chưa có, hoàn thiện chúng trước khi gọi API thật.

## Kiến trúc trước và sau tháng

| Trước Tháng 03 | Sau Tháng 03 |
|---|---|
| Route chat trả mock response | `ChatService` gọi OpenAI Responses API qua adapter tách biệt |
| Không có streaming hay usage | SSE stream; log request id, latency, model, usage và lỗi đã phân loại |
| JSON tự do | Schema Pydantic cho output có cấu trúc và fallback an toàn |
| Không có capability bên ngoài | Tool registry có hai tool chỉ-đọc, timeout, retry, budget và max vòng lặp |
| Không có giao thức kết nối công cụ | MCP server local tối thiểu có tool và resource read-only |

## Kế hoạch tuần

1. [Tuần 01 — Responses API, streaming và độ tin cậy](./Week-01.md): tạo adapter LLM, chat thật, stream và telemetry.
2. [Tuần 02 — Prompt, Structured Output và prompt regression](./Week-02.md): biến đầu ra thành contract kiểm thử được.
3. [Tuần 03 — Tool Calling có giới hạn](./Week-03.md): thêm tool registry, tool loop đóng và test lỗi.
4. [Tuần 04 — MCP server và bàn giao RAG](./Week-04.md): publish capability read-only qua MCP, demo và ghi handoff.

Mỗi tuần có bảy ngày theo đúng thứ tự; mỗi ngày chỉ có một trọng tâm, ngân sách 85–115 phút và một thay đổi kiểm thử được trong `ai-assistant-platform`. Làm các command với fake/fixture trước; chỉ thực hiện smoke test gọi API thật khi có key và quota riêng.

## Đầu ra có thể kiểm tra

- `POST /api/v1/chat` gọi LLM khi `OPENAI_API_KEY` tồn tại; khi thiếu key trả lỗi cấu hình an toàn, không log secret.
- `POST /api/v1/chat/stream` trả Server-Sent Events và kết thúc đúng khi upstream hoàn tất.
- Một service Structured Output trả `SupportAnswer` đã validate; fixture lỗi đi qua fallback rõ ràng.
- Prompt regression suite với dataset, baseline/threshold và báo cáo lỗi.
- Hai tool an toàn (`get_service_status`, `search_product_docs`) có schema, timeout, retry giới hạn, tool budget và max vòng lặp.
- MCP server local expose ít nhất một tool và một resource chỉ-đọc; client smoke test không cần production credential.

## Thiết lập an toàn

Lưu `OPENAI_API_KEY` trong `.env` cục bộ, chỉ commit `.env.example` chứa tên biến. Khởi động server bằng `uv run uvicorn app.main:app --reload`; test không gọi mạng dùng fake adapter/fixture. Lệnh gọi API thật là tùy chọn nếu có key và quota; không đưa key vào curl, log hoặc commit.

## Milestone tháng

Chạy được một demo có chat thường, chat streaming, intent/answer structured, một câu hỏi dùng tool chỉ-đọc và MCP inspector/client local. `uv run pytest`, `uv run ruff check .` pass; log cho một request mẫu có latency/usage hoặc ghi rõ `usage_unavailable`.

## Rủi ro và giảm tải

- **Thiếu API key/quota:** hoàn thành toàn bộ contract với `FakeLLMClient`; chỉ Day 4/6 cần smoke test thật.
- **Stream và tool loop quá tải:** chỉ dùng một route SSE, hai tool deterministic, tối đa hai vòng tool; không thêm framework agent.
- **Model output không ổn định:** Pydantic là boundary cuối; fixture regression không phụ thuộc đúng từng câu chữ.
- **Chi phí/latency:** ghi usage và latency trước khi tối ưu; giới hạn `max_output_tokens` và không retry lỗi validation vô hạn.

## Definition of Done tháng

- Bốn tuần có đủ 28 ngày, mỗi ngày 60–120 phút và một trọng tâm riêng.
- LLM integration, streaming, Structured Output, timeout/retry, Tool Calling, MCP, prompt regression và logging đều có command/test hoặc kiểm tra tay.
- Không có secret hard-code; tool không ghi/xóa dữ liệu và không có vòng lặp không giới hạn.
- Có đường bàn giao sang ingest/retrieval của Tháng 04, không dạy Qdrant, RAGAS hay LangGraph sớm.

## Tài liệu tham khảo đã chọn

- [OpenAI API model guidance](https://developers.openai.com/api/docs/guides/latest-model) — chọn model/configuration có chủ đích, không hard-code “latest”.
- [OpenAI Responses streaming reference](https://platform.openai.com/docs/api-reference/responses-streaming/response/function_call_arguments/done?api-mode=responses) — event stream, output item và trạng thái lỗi.
- [OpenAI Responses API reference](https://platform.openai.com/docs/api-reference/responses) — request/response, usage và input roles.
- [Pydantic model validation](https://docs.pydantic.dev/latest/concepts/models/) — validation boundary và `ValidationError`.
- [FastAPI StreamingResponse](https://fastapi.tiangolo.com/advanced/custom-response/#streamingresponse) — stream response từ generator/async generator.
- [MCP server concepts](https://modelcontextprotocol.io/docs/learn/server-concepts) và [MCP tools specification](https://modelcontextprotocol.io/specification/draft/server/tools) — tools, resources và permission boundary.

## Bàn giao Tháng 04

Giữ `LLMClient`/`ChatService` tách khỏi route. Tháng 04 sẽ thêm `app/rag/` để trả context/citation vào prompt hiện có; không thay tool registry bằng agent. File `docs/month-04-handoff.md` mô tả contract `RetrievedContext` được đề xuất và cách giữ citation trong response schema.

## Review

Xem [REVIEW.md](./REVIEW.md) để đi tới báo cáo tự review canonical.
