# Tháng 03 — Tuần 03: Tool Calling có giới hạn

## Mục tiêu tuần

Xây vòng tool calling nhỏ, tường minh và dừng được: model chỉ thấy hai tool đọc dữ liệu cục bộ, app validate input/result, giới hạn thời gian, retry và số vòng. Đây là orchestration xác định, chưa phải agent/LangGraph.

## Kiến thức và feature sẽ bổ sung

- JSON Schema tool definition, tool call id, function call output, tool error contract.
- Permission boundary, allowlist, timeout/retry per tool, tool budget và max iterations.
- `src/ai_assistant_platform/tools/registry.py`, `src/ai_assistant_platform/tools/status.py`, `src/ai_assistant_platform/tools/docs.py`, `src/ai_assistant_platform/services/tool_chat_service.py`.

## Kế hoạch từng ngày

### Ngày 15 — Thiết kế tool permission boundary

**Tài liệu:** đọc [OpenAI function calling](https://platform.openai.com/docs/guides/function-calling), phần tool definition; đối chiếu với permission matrix của ứng dụng.

- **Mục tiêu:** chọn capability an toàn trước tool schema.
- **Kết quả cần đạt:** registry chỉ chứa `get_service_status` và `search_product_docs`, đều read-only, deterministic từ fixture.
- **Thời lượng (85 phút):** 20 phút đọc function/tool concept, 40 phút design/code, 15 phút test, 10 phút ghi chú.
- **Lý thuyết:** tool description không phải authorization; capability nhỏ hơn endpoint.
- **Bài thực hành:** viết `ToolDefinition` với `side_effects=False`.
- **Tích hợp project:** tool registry độc lập LLM provider.
- **File:** `src/ai_assistant_platform/tools/contracts.py`, `src/ai_assistant_platform/tools/registry.py`, `docs/tool-permissions.md`, `tests/unit/test_tool_registry.py`.
- **Lệnh:** `uv run pytest tests/unit/test_tool_registry.py -q`.
- **Kết quả mong đợi:** unknown tool bị reject.
- **Kiểm tra:** assert không có write/delete/network-admin tool.
- **DoD:** permission matrix ghi tool, input, dữ liệu, side effect.
- **Commit:** `feat(tools): add read-only tool registry`.
- **Tự kiểm tra:** Schema có thay thế authorization không? Vì sao không expose filesystem tool?

### Ngày 16 — Tool schema và input validation

**Tài liệu:** xem [Pydantic JSON Schema](https://docs.pydantic.dev/latest/concepts/json_schema/), phần schema sinh từ model.

- **Mục tiêu:** convert Pydantic input thành schema và validate lại trước execution.
- **Kết quả cần đạt:** `SearchDocsInput(query, limit≤3)` không nhận extra field.
- **Thời lượng (95 phút):** 20 phút schema theory, 50 phút code, 15 phút test, 10 phút ghi chú.
- **Lý thuyết:** model-generated arguments là untrusted input.
- **Bài thực hành:** tạo OpenAI-compatible function definition từ JSON schema.
- **Tích hợp project:** registry trả schema cho adapter.
- **File:** `src/ai_assistant_platform/tools/schemas.py`, `src/ai_assistant_platform/tools/registry.py`, `tests/unit/test_tool_schemas.py`.
- **Lệnh:** `uv run pytest tests/unit/test_tool_schemas.py -q`.
- **Kết quả mong đợi:** `{limit:99}` và extra property fail trước handler.
- **Kiểm tra:** print schema, kiểm tra `additionalProperties` bị cấm qua validation model.
- **DoD:** handler không nhận raw dict.
- **Commit:** `feat(tools): validate function tool inputs`.
- **Tự kiểm tra:** Tại sao model output là input không tin cậy? Limit nhỏ bảo vệ điều gì?

### Ngày 17 — Tool status chỉ-đọc và result contract

**Tài liệu:** đọc [OpenAI function calling](https://platform.openai.com/docs/guides/function-calling), phần xử lý function output.

- **Mục tiêu:** implement tool đầu tiên có output kiểm thử được.
- **Kết quả cần đạt:** `get_service_status` trả service name, health và checked_at từ clock injectable.
- **Thời lượng (90 phút):** 15 phút lý thuyết result contract, 50 phút code/test, 15 phút inspect, 10 phút ghi chú.
- **Bài thực hành:** handler không gọi HTTP thật; đọc health service/fixture.
- **Tích hợp project:** status tool tái dùng readiness logic hiện có.
- **File:** `src/ai_assistant_platform/tools/status.py`, `src/ai_assistant_platform/tools/results.py`, `tests/unit/test_status_tool.py`.
- **Lệnh:** `uv run pytest tests/unit/test_status_tool.py -q`.
- **Kết quả mong đợi:** output có schema stable và no secret.
- **Kiểm tra:** injected clock tạo timestamp cố định.
- **DoD:** error result khác success result.
- **Commit:** `feat(tools): add service status tool`.
- **Tự kiểm tra:** Tool result cần ít field hơn endpoint response vì sao? Làm sao test time?

### Ngày 18 — Tool tìm tài liệu cục bộ

**Tài liệu:** xem lại [OpenAI function calling](https://platform.openai.com/docs/guides/function-calling), phần tool result; chỉ dùng fixture local trong ngày này.

- **Mục tiêu:** thêm tool đọc catalog an toàn, không biến thành web search.
- **Kết quả cần đạt:** `search_product_docs` tìm top 3 đoạn trong fixture product docs, kèm document id/title.
- **Thời lượng (105 phút):** 20 phút thiết kế deterministic search, 55 phút code, 20 phút test, 10 phút ghi chú.
- **Lý thuyết:** source attribution sơ bộ và boundary dữ liệu.
- **Bài thực hành:** case-insensitive keyword matching, empty result hợp lệ.
- **Tích hợp project:** tạo catalog sẽ được thay bằng retrieval Month 04.
- **File:** `src/ai_assistant_platform/tools/docs.py`, `src/ai_assistant_platform/data/product_docs.json`, `tests/unit/test_docs_tool.py`.
- **Lệnh:** `uv run pytest tests/unit/test_docs_tool.py -q`.
- **Kết quả mong đợi:** query khớp trả tối đa 3 result, query lạ trả list rỗng.
- **Kiểm tra:** input không thể truyền path/URL.
- **DoD:** ghi rõ tool này không phải RAG.
- **Commit:** `feat(tools): add safe local docs search`.
- **Tự kiểm tra:** Tại sao đây chưa là vector retrieval? Document id giúp Month 04 thế nào?

### Ngày 19 — Execute tool với timeout và error envelope

**Tài liệu:** đọc [Python asyncio timeout](https://docs.python.org/3/library/asyncio-task.html#asyncio.timeout), phần cancellation và timeout context manager.

- **Mục tiêu:** chạy handler qua executor có deadline.
- **Kết quả cần đạt:** success, validation, timeout và unexpected error thành `ToolExecutionResult` phân biệt được.
- **Thời lượng (105 phút):** 25 phút async timeout, 50 phút executor, 20 phút test, 10 phút ghi chú.
- **Lý thuyết:** timeout/cancellation; error message không leak implementation.
- **Bài thực hành:** slow fake handler ngủ vượt deadline.
- **Tích hợp project:** tất cả tool đi qua executor, không gọi handler trực tiếp từ service.
- **File:** `src/ai_assistant_platform/tools/executor.py`, `src/ai_assistant_platform/tools/errors.py`, `tests/unit/test_tool_executor.py`.
- **Lệnh:** `uv run pytest tests/unit/test_tool_executor.py -q`.
- **Kết quả mong đợi:** timeout result có `retryable` theo policy.
- **Kiểm tra:** unexpected exception không xuất hiện stack trace trong tool output.
- **DoD:** timeout là settings, không literal ở handler.
- **Commit:** `feat(tools): add timeout-safe tool executor`.
- **Tự kiểm tra:** Timeout upstream khác timeout tool thế nào? Tool error nào model có thể xử lý?

### Ngày 20 — Vòng function calling đóng

**Tài liệu:** đọc [OpenAI function calling](https://platform.openai.com/docs/guides/function-calling), phần gửi tool output về model.

- **Mục tiêu:** nối function call → executor → function output → final response.
- **Kết quả cần đạt:** fake LLM yêu cầu một tool rồi nhận tool result và trả final answer.
- **Thời lượng (115 phút):** 25 phút đọc flow, 60 phút orchestrator, 20 phút test, 10 phút ghi chú.
- **Lý thuyết:** preserve call id; model quyết định call nhưng app kiểm soát execution.
- **Bài thực hành:** model fake emits `search_product_docs`, tiếp turn sees result.
- **Tích hợp project:** thêm `ToolChatService`, không sửa Structured endpoint.
- **File:** `src/ai_assistant_platform/services/tool_chat_service.py`, `src/ai_assistant_platform/llm/tool_protocol.py`, `tests/unit/test_tool_chat_service.py`.
- **Lệnh:** `uv run pytest tests/unit/test_tool_chat_service.py -q`.
- **Kết quả mong đợi:** history có đúng call id và output; final answer trả về.
- **Kiểm tra:** malformed call argument không gọi handler.
- **DoD:** only allowlisted registry can execute.
- **Commit:** `feat(chat): orchestrate one safe tool call`.
- **Tự kiểm tra:** Call id dùng để làm gì? Vì sao app không “tin” tool name của model?

### Ngày 21 — Tool budget, max loop và milestone failure tests

**Tài liệu:** xem [OpenAI function calling](https://platform.openai.com/docs/guides/function-calling), phần thực thi tool do application kiểm soát.

- **Mục tiêu:** đảm bảo tool workflow luôn dừng.
- **Kết quả cần đạt:** tối đa 2 call/1 request, tối đa 2 iteration, retry mỗi tool tối đa 1; báo lỗi rõ khi vượt.
- **Thời lượng (110 phút):** 20 phút design budget, 55 phút guard/test, 20 phút run suite, 15 phút review.
- **Lý thuyết:** tool calling khác agent autonomy.
- **Bài thực hành:** fake yêu cầu tool vô hạn/unknown/timeout để test stop condition.
- **Tích hợp project:** config `ToolExecutionLimits` và telemetry `tool_calls`, `tool_failures`.
- **File:** `src/ai_assistant_platform/core/tool_limits.py`, `src/ai_assistant_platform/services/tool_chat_service.py`, `tests/unit/test_tool_limits.py`, `docs/tool-workflow.md`.
- **Lệnh:** `uv run pytest tests/unit/test_tool_chat_service.py tests/unit/test_tool_limits.py -q`; `uv run ruff check .`.
- **Kết quả mong đợi:** every adversarial fixture terminates predictably.
- **Kiểm tra:** assert handler count không vượt budget.
- **DoD:** README ghi rõ đây chưa có autonomous loop.
- **Commit:** `feat(tools): enforce call budget and max iterations`.
- **Tự kiểm tra:** Budget khác max iteration thế nào? Tại sao tool retry cũng cần budget?

## Milestone, review và DoD

- **Milestone:** demo offline một answer dùng status/docs tool; test chứng minh reject unknown input, timeout và loop vô hạn.
- **Review checklist:** [ ] hai tool read-only; [ ] validate hai lần (schema + executor); [ ] timeout/budget tested; [ ] call id preserved; [ ] không có network write.
- **Definition of Done:** app kiểm soát capability, không phải model.
- **Lỗi thường gặp:** expose tool quá rộng, tin JSON model, retry side effect, cho loop không giới hạn.
- **Tùy chọn (≤30 phút):** thêm metric tool success rate từ fake fixtures.
- **Tài liệu:** Responses streaming/reference và MCP tools concepts trong [README tháng](./README.md#tài-liệu-tham-khảo-đã-chọn).
