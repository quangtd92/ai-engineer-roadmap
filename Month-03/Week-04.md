# Tháng 03 — Tuần 04: MCP server, demo và bàn giao RAG

## Mục tiêu tuần

Hiểu MCP như giao thức kết nối capability, không như framework agent. Publish lại capability read-only qua MCP server tối thiểu, kiểm tra bằng client local, sau đó dọn contract và bàn giao catalog cho RAG Month 04.

## Kiến thức và feature sẽ bổ sung

- Vai trò host/client/server, tools vs resources vs prompts, transport local và capability negotiation ở mức khái niệm.
- MCP tool/resource schemas, read-only boundary, audit log và không cấp filesystem/network credential.
- `src/ai_assistant_platform/mcp/server.py`, MCP tool `search_product_docs`, resource `assistant://product-docs/catalog` và smoke test.

## Kế hoạch từng ngày

### Ngày 22 — MCP mental model và ranh giới bảo mật

**Tài liệu:** đọc [MCP server concepts](https://modelcontextprotocol.io/docs/learn/server-concepts), phần host, client, server và capability.

**Mục tiêu:** phân biệt MCP server với OpenAI function tool và agent. **Kết quả cần đạt:** ADR ngắn mô tả host/client/server, tool/resource và lý do chỉ expose catalog read-only. **Thời lượng (85 phút):** 30 phút đọc [MCP server concepts](https://modelcontextprotocol.io/docs/learn/server-concepts), 35 phút sơ đồ/ADR, 10 phút review, 10 phút ghi chú. **Lý thuyết:** client/application chọn resources; tool có thể model-controlled nhưng phải bị app giới hạn. **Bài thực hành:** vẽ sequence local: client discover → call tool → receive result. **Tích hợp project:** tái sử dụng `src/ai_assistant_platform/tools/docs.py`, không tạo logic tìm kiếm thứ hai. **File:** `docs/adr/0003-mcp-read-only-boundary.md`, `docs/mcp-sequence.md`. **Lệnh:** `uv run python -m compileall src/ai_assistant_platform`. **Kết quả mong đợi:** ADR nêu rõ không expose shell, filesystem write, API key hay user data. **Kiểm tra:** đọc ADR và chỉ ra capability nào bị từ chối. **DoD:** không dùng LangGraph/agent terminology cho MCP. **Commit:** `docs(mcp): define read-only server boundary`. **Tự kiểm tra:** MCP server khác function registry ở đâu? Resource khác tool thế nào?

### Ngày 23 — Skeleton MCP server và discovery

**Tài liệu:** đọc [MCP server concepts](https://modelcontextprotocol.io/docs/learn/server-concepts), phần capability discovery và server boundaries.

**Mục tiêu:** khởi tạo server local có danh sách capability. **Kết quả cần đạt:** server expose metadata/name/version và client test thấy tool/resource list. **Thời lượng (105 phút):** 25 phút đọc specification overview, 55 phút setup/code, 15 phút test, 10 phút ghi chú. **Lý thuyết:** JSON-RPC lifecycle/capability discovery ở mức overview. **Bài thực hành:** cài MCP SDK theo tài liệu SDK được chọn trong `pyproject.toml`; sử dụng stdio/local transport. **Tích hợp project:** server ở `src/ai_assistant_platform/mcp`, import service read-only qua dependency. **File:** `pyproject.toml`, `uv.lock`, `src/ai_assistant_platform/mcp/server.py`, `tests/integration/test_mcp_discovery.py`. **Lệnh:** `uv run pytest tests/integration/test_mcp_discovery.py -q`. **Kết quả mong đợi:** discovery trả capability đã đăng ký, không cần OpenAI key. **Kiểm tra:** server import thành công khi `OPENAI_API_KEY` thiếu. **DoD:** transport không bind public network trong bài này. **Commit:** `feat(mcp): add local server discovery`. **Tự kiểm tra:** Vì sao stdio giảm bề mặt tấn công khi học? Discovery giúp client gì?

### Ngày 24 — MCP tool bọc local docs search

**Tài liệu:** đọc [MCP tools specification](https://modelcontextprotocol.io/specification/draft/server/tools), phần input schema và error response.

**Mục tiêu:** expose `search_product_docs` qua MCP với schema nhất quán. **Kết quả cần đạt:** MCP call input hợp lệ trả list title/document id/snippet; input sai bị error có mã ổn định. **Thời lượng (105 phút):** 20 phút đọc MCP tools schema, 55 phút handler/mapper, 20 phút test, 10 phút ghi chú. **Lý thuyết:** JSON Schema, structured result và không chuyển raw exception. **Bài thực hành:** map Pydantic validation sang MCP error result. **Tích hợp project:** gọi chính handler Week 03, không duplicate search. **File:** `src/ai_assistant_platform/mcp/tools.py`, `src/ai_assistant_platform/mcp/server.py`, `tests/integration/test_mcp_docs_tool.py`. **Lệnh:** `uv run pytest tests/integration/test_mcp_docs_tool.py -q`. **Kết quả mong đợi:** same query có kết quả tương đương HTTP tool. **Kiểm tra:** `limit=100` fail và handler không chạy. **DoD:** tool metadata nêu read-only/data source. **Commit:** `feat(mcp): expose safe docs search tool`. **Tự kiểm tra:** Vì sao MCP schema vẫn không phải authorization? Mapping exception nên giữ lại điều gì?

### Ngày 25 — MCP resource catalog

**Tài liệu:** đọc [MCP resources specification](https://modelcontextprotocol.io/specification/draft/server/resources), phần list/read resource và MIME type.

**Mục tiêu:** expose context passive thay vì một tool nữa. **Kết quả cần đạt:** resource URI cố định `assistant://product-docs/catalog` trả metadata catalog, không trả toàn bộ secret/config. **Thời lượng (95 phút):** 20 phút đọc MCP resources, 50 phút code/test, 15 phút inspect output, 10 phút ghi chú. **Lý thuyết:** resource application-controlled, URI/MIME type. **Bài thực hành:** tạo resource list/read với JSON metadata. **Tích hợp project:** catalog chuẩn bị cho ingest/versioning Month 04. **File:** `src/ai_assistant_platform/mcp/resources.py`, `src/ai_assistant_platform/mcp/server.py`, `tests/integration/test_mcp_resources.py`. **Lệnh:** `uv run pytest tests/integration/test_mcp_resources.py -q`. **Kết quả mong đợi:** list có URI/title/mime type và read trả JSON hợp lệ. **Kiểm tra:** assert resource không include full `.env`/filesystem path. **DoD:** resource là read-only snapshot. **Commit:** `feat(mcp): publish product docs catalog resource`. **Tự kiểm tra:** Khi nào dùng resource thay tool? URI ổn định có ích gì?

### Ngày 26 — MCP audit logging và negative tests

**Tài liệu:** đọc [MCP tools specification](https://modelcontextprotocol.io/specification/draft/server/tools), phần security considerations và error handling.

**Mục tiêu:** quan sát server mà không log sensitive input. **Kết quả cần đạt:** event log có correlation id, capability, outcome, latency nhưng query được hash/redact theo policy. **Thời lượng (100 phút):** 20 phút privacy design, 50 phút instrumentation/tests, 20 phút adversarial cases, 10 phút ghi chú. **Lý thuyết:** auditability không đồng nghĩa lưu nội dung người dùng. **Bài thực hành:** test unknown tool, invalid argument và resource URI lạ. **Tích hợp project:** dùng telemetry format Week 01. **File:** `src/ai_assistant_platform/mcp/telemetry.py`, `src/ai_assistant_platform/mcp/server.py`, `tests/unit/test_mcp_telemetry.py`, `tests/integration/test_mcp_negative_cases.py`. **Lệnh:** `uv run pytest tests/unit/test_mcp_telemetry.py tests/integration/test_mcp_negative_cases.py -q`. **Kết quả mong đợi:** denied request có audit event, không stack trace. **Kiểm tra:** fixture query `secret=abc` không xuất hiện nguyên văn trong log. **DoD:** capability failures không làm server crash. **Commit:** `feat(mcp): audit capability access safely`. **Tự kiểm tra:** Audit log khác application log ở đâu? Vì sao hash không luôn là anonymization?

### Ngày 27 — Demo end-to-end và documentation

**Tài liệu:** đọc lại [MCP server concepts](https://modelcontextprotocol.io/docs/learn/server-concepts) và checklist test offline của tuần này.

**Mục tiêu:** thực hiện demo lặp lại được không cần network credential. **Kết quả cần đạt:** hướng dẫn chạy API fake, test tool workflow và MCP discovery/tool/resource smoke tests. **Thời lượng (110 phút):** 15 phút chuẩn bị, 55 phút demo script/docs, 25 phút run full suite, 15 phút sửa. **Lý thuyết:** smoke test khác evaluation; demo cần deterministic. **Bài thực hành:** tạo `scripts/demo_month_03.py` dùng fake + local client test. **Tích hợp project:** README project thêm section Month 03 commands/boundary. **File:** `scripts/demo_month_03.py`, `README.md`, `docs/mcp-demo.md`. **Lệnh:** `uv run python scripts/demo_month_03.py`; `uv run pytest`; `uv run ruff check .`. **Kết quả mong đợi:** script in từng checkpoint PASS/FAIL và không yêu cầu key. **Kiểm tra:** chạy trong environment không có `OPENAI_API_KEY`. **DoD:** docs nêu chat thật là smoke test tùy chọn. **Commit:** `docs(demo): add month three offline walkthrough`. **Tự kiểm tra:** Vì sao demo fake vẫn giá trị? Những gì demo này chưa chứng minh?

### Ngày 28 — Review, refactor và bàn giao Month 04

**Tài liệu:** xem [README tháng](./README.md#bàn-giao-tháng-04) và [MCP resources specification](https://modelcontextprotocol.io/specification/draft/server/resources) để chốt interface catalog.

**Mục tiêu:** chốt contract LLM/tool/MCP và chuẩn bị RAG không phá vỡ API. **Kết quả cần đạt:** handoff mô tả `RetrievedContext`, citation fields, catalog versioning và backlog đã loại khỏi Month 03. **Thời lượng (105 phút):** 25 phút review checklists, 35 phút refactor nhỏ, 25 phút full validation, 20 phút handoff. **Lý thuyết:** retrieval sẽ thay keyword catalog, không thay error/budget boundary. **Bài thực hành:** cập nhật import/dead code sau test; không thêm Qdrant. **Tích hợp project:** tạo interface stub/document cho `src/ai_assistant_platform/rag/` tương lai, chưa tạo implementation. **File:** `docs/month-04-handoff.md`, `README.md`, test liên quan. **Lệnh:** `uv run pytest`; `uv run ruff check .`; `uv run python scripts/run_prompt_regression.py`. **Kết quả mong đợi:** full suite pass; handoff chỉ ra input/output giữ ổn định. **Kiểm tra:** đọc handoff và xác định được Day 1 Month 04 cần làm gì mà không có technology jump. **DoD:** không để hạng mục dở dang; RAG/agent không bị đưa vào Month 03. **Commit:** `docs(month-03): record llm tooling baseline and rag handoff`. **Tự kiểm tra:** RAG sẽ thay phần nào trong tool? Tại sao không biến MCP server thành agent?

## Milestone, review và DoD

**Milestone:** local MCP server discover được, gọi docs tool và đọc catalog resource; toàn bộ demo/test offline pass. **Review checklist:** [ ] server local-only; [ ] tool/resource read-only; [ ] negative tests; [ ] audit redaction; [ ] handoff không đòi Qdrant trước khi Week 01 Month 04. **Definition of Done:** MCP capability là wrapper tối thiểu cho capability hiện có, có schema, error behavior và boundary rõ. **Lỗi thường gặp:** nhầm resource là tool, mở network public, duplicate business logic, coi MCP là agent, log query nhạy cảm. **Tùy chọn (≤30 phút):** mở MCP Inspector chỉ để quan sát discovery nếu môi trường đã có, không thêm dependency bắt buộc. **Tài liệu:** [MCP server concepts](https://modelcontextprotocol.io/docs/learn/server-concepts), [tools specification](https://modelcontextprotocol.io/specification/draft/server/tools), [resources specification](https://modelcontextprotocol.io/specification/draft/server/resources).
