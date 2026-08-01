# Tháng 5 — Tuần 2: Checkpoint, persistence và memory theo thread

## Mục tiêu tuần

Làm cho graph xác định của Tuần 1 có thể dừng và tiếp tục theo `thread_id`. Tuần này chỉ lưu state nghiệp vụ và lịch sử hội thoại ngắn hạn; không tự ghi sở thích người dùng vào long-term memory.

## Kiến thức cần đạt

- Checkpoint là snapshot versioned của graph, khác cache và khác database nghiệp vụ.
- `thread_id` là khóa cô lập hội thoại; client/API key/database connection không được checkpoint.
- Short-term memory phải có cửa sổ, trimming hoặc summary để không phình context. Long-term memory cần consent và chỉ học overview.

## Tính năng project sẽ bổ sung

`app/services/checkpoints.py`, checkpointer factory, `GET /api/v1/agent/threads/{thread_id}`, memory policy và các integration test resume. In-memory saver là baseline test; adapter PostgreSQL được cấu hình bằng environment, không hard-code DSN.

## Kế hoạch từng ngày

### Ngày 8 — Định nghĩa hợp đồng checkpoint

- **Mục tiêu cụ thể:** Xác định state nào được lưu và lifecycle của một thread.
- **Kết quả cần đạt:** Có ADR mô tả `thread_id`, checkpoint namespace, retention 7 ngày cho demo, dữ liệu bị cấm lưu và quy tắc xóa thủ công.
- **Phân bổ thời gian:** 15 phút xem state Tuần 1, 25 phút đọc, 45 phút ADR/schema, 20 phút review (105 phút).
- **Lý thuyết cần học:** Checkpoint lưu state để resume/debug; nó không thay thế audit log, authorization hay memory vĩnh viễn.
- **Tài liệu cần đọc:** Phần “Threads” và “Checkpoints” trong [Persistence](./RESOURCES.md).
- **Bài thực hành:** Liệt kê từng key `AgentState` là persist/ephemeral/redacted; thêm validator UUID/slug cho `thread_id`.
- **Tích hợp project:** Mở rộng `AgentRunRequest` để bắt buộc `thread_id` do client tạo hoặc server sinh rồi trả về.
- **File tạo/sửa:** `docs/adr/006-agent-checkpoint-contract.md`, `app/api/schemas/agent.py`, `tests/unit/test_thread_id.py`.
- **Lệnh chạy:** `uv run pytest tests/unit/test_thread_id.py -q`.
- **Kết quả mong đợi:** ID rỗng/quá dài bị 422; schema không có API key, raw authorization header hoặc client object.
- **Cách tự kiểm tra:** Serialize request/state fixture và tìm bằng `rg "api_key|authorization" app/agents tests/unit/test_thread_id.py`.
- **Definition of Done:** ADR nêu retention, ownership và cách xử lý `thread_id` không hợp lệ.
- **Commit message gợi ý:** `docs(agent): define checkpoint and thread contract`.
- **Câu hỏi tự kiểm tra:** Vì sao `thread_id` không được là email? Checkpoint khác audit log ra sao?

### Ngày 9 — Gắn InMemorySaver cho graph

- **Mục tiêu cụ thể:** Compile graph với checkpointer nhỏ, tái lập được trong test.
- **Kết quả cần đạt:** Cùng `thread_id` ghi checkpoint sau mỗi node; thread khác không đọc được state của nhau.
- **Phân bổ thời gian:** 20 phút đọc, 50 phút code, 25 phút unit test, 10 phút ghi chú (105 phút).
- **Lý thuyết cần học:** Configurable `thread_id` tách configuration runtime khỏi state; saver dùng cho test không chứng minh durability sau process restart.
- **Tài liệu cần đọc:** Ví dụ checkpointer tối thiểu trong [Persistence](./RESOURCES.md).
- **Bài thực hành:** Tạo `build_agent_graph(checkpointer)`; truyền `{"configurable": {"thread_id": ...}}` khi invoke thay vì nhét ID vào global.
- **Tích hợp project:** `AgentService.run()` nhận checkpointer qua dependency injection để test dùng `InMemorySaver`.
- **File tạo/sửa:** `app/agents/graph.py`, `app/services/checkpoints.py`, `tests/unit/test_agent_checkpoints.py`.
- **Lệnh chạy:** `uv run pytest tests/unit/test_agent_checkpoints.py -q`.
- **Kết quả mong đợi:** Test đọc được snapshot cuối của đúng thread và không thấy query của thread khác.
- **Cách tự kiểm tra:** Chạy hai fixture xen kẽ; assert số checkpoint tăng nhưng state không dùng mutable global.
- **Definition of Done:** Graph vẫn pass test routing Tuần 1 khi không thay logic route.
- **Commit message gợi ý:** `feat(agent): checkpoint graph state by thread`.
- **Câu hỏi tự kiểm tra:** Vì sao checkpointer là dependency? `thread_id` nằm trong config hay state vì sao?

### Ngày 10 — Đọc state history và debug replay

- **Mục tiêu cụ thể:** Cho phép quan sát lịch sử state có kiểm soát để debug workflow.
- **Kết quả cần đạt:** Service trả metadata checkpoint theo thứ tự mới nhất, có `step_count`, route và status; response không trả document text/raw prompt.
- **Phân bổ thời gian:** 15 phút ôn saver, 25 phút đọc, 50 phút service/test, 15 phút review (105 phút).
- **Lý thuyết cần học:** History hỗ trợ debug khi state transition rõ; replay dùng cùng input/config, không dùng để chạy lại side effect.
- **Tài liệu cần đọc:** Phần “Get state” và “Get state history” trong [Persistence](./RESOURCES.md).
- **Bài thực hành:** Viết mapper từ snapshot sang `ThreadCheckpointSummary`; giới hạn 20 record và sort xác định.
- **Tích hợp project:** Thêm endpoint nội bộ `GET /api/v1/agent/threads/{thread_id}/checkpoints` có response model.
- **File tạo/sửa:** `app/services/agent_threads.py`, `app/api/routes/agent.py`, `tests/integration/test_agent_thread_history.py`.
- **Lệnh chạy:** `uv run pytest tests/integration/test_agent_thread_history.py -q`.
- **Kết quả mong đợi:** Endpoint trả 404 cho thread lạ, 200 cho thread fixture và không lộ `documents`/message nội bộ.
- **Cách tự kiểm tra:** Assert JSON keys whitelist và snapshot order trong integration test.
- **Definition of Done:** History có pagination/limit rõ ràng và không trở thành endpoint export dữ liệu hội thoại.
- **Commit message gợi ý:** `feat(agent): expose redacted checkpoint history`.
- **Câu hỏi tự kiểm tra:** Tại sao không trả full state cho frontend? Replay nào cần approval lại?

### Ngày 11 — Short-term memory và trimming

- **Mục tiêu cụ thể:** Giữ ngữ cảnh hội thoại hữu ích trong giới hạn token/message.
- **Kết quả cần đạt:** Policy giữ 6 message gần nhất và system context; message cũ bị trim có record `memory_trimmed=true`.
- **Phân bổ thời gian:** 20 phút đọc, 45 phút implement, 30 phút tests, 10 phút note (105 phút).
- **Lý thuyết cần học:** Short-term memory thuộc thread; trimming giảm cost/latency nhưng có thể mất ngữ cảnh, nên phải đo và minh bạch.
- **Tài liệu cần đọc:** Phần short-term memory và trimming trong [Memory](./RESOURCES.md).
- **Bài thực hành:** Viết pure function `trim_messages(messages, max_messages)`; bảo toàn role/system và không tóm tắt bằng LLM trong scope hôm nay.
- **Tích hợp project:** Node trước `draft` dùng policy này và thêm `memory_summary` rỗng thay vì suy diễn nội dung đã bỏ.
- **File tạo/sửa:** `app/agents/memory.py`, `app/agents/nodes.py`, `tests/unit/test_agent_memory.py`.
- **Lệnh chạy:** `uv run pytest tests/unit/test_agent_memory.py -q`.
- **Kết quả mong đợi:** Fixture 9 message còn đúng 6 message được phép; prompt injection cũ không quay lại từ buffer.
- **Cách tự kiểm tra:** Test role ordering, empty history, over-limit và đảm bảo token/raw message không bị log.
- **Definition of Done:** Memory bound là hằng cấu hình có test, không phải magic number trong node.
- **Commit message gợi ý:** `feat(agent): bound short-term thread memory`.
- **Câu hỏi tự kiểm tra:** Trimming có phải long-term memory không? Mất ngữ cảnh được phát hiện thế nào?

### Ngày 12 — Adapter persistence PostgreSQL và migration an toàn

- **Mục tiêu cụ thể:** Tạo boundary để thay InMemorySaver bằng persistence bền vững mà không đổi business graph.
- **Kết quả cần đạt:** Factory chọn `memory` hoặc `postgres` bằng Settings; Postgres checkpointer có health/config test và DSN chỉ đọc từ env.
- **Phân bổ thời gian:** 20 phút đọc, 45 phút adapter/config, 30 phút test fake, 15 phút migration note (110 phút).
- **Lý thuyết cần học:** PostgreSQL phù hợp checkpoint durable; Redis phù hợp transient/cache. Migration phải idempotent và được chạy như bước deploy, không tự chạy mỗi request.
- **Tài liệu cần đọc:** Phần database setup trong [Persistence](./RESOURCES.md) và memory persistence trong [Memory](./RESOURCES.md).
- **Bài thực hành:** Khai báo protocol `CheckpointStore`; thêm `CHECKPOINTER_BACKEND` và `DATABASE_URL` vào `.env.example` chỉ với tên biến; viết `docs/checkpoints.md` hướng dẫn migration.
- **Tích hợp project:** `create_app()` build checkpointer từ factory, test mặc định vẫn dùng in-memory không cần database thật.
- **File tạo/sửa:** `app/services/checkpoints.py`, `app/core/settings.py`, `.env.example`, `docs/checkpoints.md`, `tests/unit/test_checkpoint_factory.py`.
- **Lệnh chạy:** `uv run pytest tests/unit/test_checkpoint_factory.py -q`; `uv run ruff check app/services/checkpoints.py`.
- **Kết quả mong đợi:** Backend không hợp lệ fail fast; thiếu DSN khi chọn Postgres cho lỗi cấu hình không lộ secret.
- **Cách tự kiểm tra:** `rg -n "postgres(ql)?://.+:.+@|sk-" .env.example docs app` không có credential thật.
- **Definition of Done:** Tài liệu ghi Postgres là persistence bắt buộc cho production sau này; Redis chỉ là lựa chọn transient đã giới thiệu, không phải framework mới.
- **Commit message gợi ý:** `feat(agent): add configurable durable checkpoint adapter`.
- **Câu hỏi tự kiểm tra:** Vì sao không auto-migrate trong node? Redis và Postgres khác nhau ở durability nào?

### Ngày 13 — Milestone: resume sau process restart mô phỏng

- **Mục tiêu cụ thể:** Chứng minh contract persistence bằng integration test trước khi sang HITL.
- **Kết quả cần đạt:** Run đầu dừng sau checkpoint; app/service instance mới dùng cùng durable store đọc được state và tiếp tục đúng thread.
- **Phân bổ thời gian:** 15 phút chuẩn bị fixture, 55 phút integration test, 25 phút run manual, 15 phút handoff (110 phút).
- **Lý thuyết cần học:** Persistence chỉ có giá trị khi một instance mới resume được; in-memory test không thay thế test adapter durable.
- **Tài liệu cần đọc:** Phần fault tolerance trong [Persistence](./RESOURCES.md).
- **Bài thực hành:** Dùng test container/local PostgreSQL nếu đã có Compose, nếu chưa có thì mark integration `requires_postgres` và chạy fake contract test; không dùng database cá nhân.
- **Tích hợp project:** Viết `docs/month-05-week-02-handoff.md` nêu checkpoint config, retention và API contract cho interrupt tuần 3.
- **File tạo/sửa:** `tests/integration/test_agent_resume.py`, `tests/integration/conftest.py`, `docs/month-05-week-02-handoff.md`.
- **Lệnh chạy:** `uv run pytest tests/integration/test_agent_resume.py -q`; `uv run pytest tests/unit/test_agent_checkpoints.py -q`.
- **Kết quả mong đợi:** Durable test pass khi dependency sẵn sàng hoặc skip có lý do; unit contract luôn pass offline.
- **Cách tự kiểm tra:** Khởi tạo factory hai lần, assert instance thứ hai thấy route/step count của thread A nhưng không thấy thread B.
- **Definition of Done:** Không tuyên bố durable pass nếu Postgres chưa chạy; hướng dẫn Compose prerequisite được ghi rõ.
- **Commit message gợi ý:** `test(agent): verify checkpoint resume across service restart`.
- **Câu hỏi tự kiểm tra:** Test nào chứng minh durability thật? Khi skip integration, chất lượng nào vẫn được đảm bảo?

### Ngày 14 — Review/buffer: privacy và handoff persistence

- **Mục tiêu cụ thể:** Rà retention, memory limit và các test trước khi đưa interrupt vào graph.
- **Kết quả cần đạt:** Checkpoint contract, API history, trimming và resume test được review; backlog không chứa long-term memory tự động.
- **Phân bổ thời gian:** 20 phút đọc diff, 30 phút chạy suite, 25 phút sửa nhỏ, 15 phút handoff (90 phút).
- **Lý thuyết cần học:** Long-term memory là quyết định sản phẩm/privacy, không phải mặc định kỹ thuật cho mọi chat.
- **Tài liệu cần đọc:** Phần long-term memory/namespace trong [LangGraph memory concepts](./RESOURCES.md).
- **Bài thực hành:** Thêm test retention config không âm, sửa naming không nhất quán và viết note “chưa triển khai” cho semantic memory.
- **Tích hợp project:** Cập nhật architecture doc: `thread_id -> checkpointer -> state history`, chỉ rõ approval sẽ checkpoint trước side effect ở Tuần 3.
- **File tạo/sửa:** `docs/architecture/agent-workflow.md`, `tests/unit/test_agent_memory.py`, `docs/month-05-week-02-handoff.md`.
- **Lệnh chạy:** `uv run pytest tests/unit/test_agent_state.py tests/unit/test_agent_checkpoints.py tests/unit/test_agent_memory.py -q`; `uv run ruff check .`.
- **Kết quả mong đợi:** Suite pass, diagram khớp graph và không có secret/checkpoint fixture thật trong repo.
- **Cách tự kiểm tra:** Đọc lại ADR Ngày 8 rồi tìm mỗi policy có test hoặc owner rõ.
- **Definition of Done:** Có thể giải thích ranh giới checkpoint, short-term và long-term memory bằng implementation hiện có.
- **Commit message gợi ý:** `refactor(agent): review persistence and memory boundaries`.
- **Câu hỏi tự kiểm tra:** Vì sao approval cần durable checkpoint? Retention chịu trách nhiệm bởi module nào?

## Milestone cuối tuần

Graph lưu checkpoint theo thread, giới hạn short-term memory, đọc được history đã redact và có contract test resume. Durable persistence được thiết kế/configure rõ ràng, không giả định một database thật luôn có sẵn.

## Review checklist

- [ ] `thread_id` được validate và cô lập state giữa các thread.
- [ ] State checkpoint JSON-serializable, không chứa secret/client/request object.
- [ ] Có checkpointer baseline và adapter durable có config/migration note.
- [ ] Memory có giới hạn/test; long-term memory chỉ overview.
- [ ] History API redact dữ liệu và giới hạn kết quả.
- [ ] Resume test phân biệt durable integration với offline contract test.

## Definition of Done

Hoàn thành bảy ngày; checkpoint, history, memory và resume có test/verification; handoff mô tả đúng contract để Tuần 3 thêm interrupt mà không thay state boundary.

## Lỗi thường gặp

- Dùng `thread_id` dự đoán được hoặc đưa email/raw user ID vào log.
- Cất LLM client, coroutine hay database connection trong state.
- Gọi mọi history là “memory” rồi không đặt retention.
- Khẳng định restart-safe chỉ vì InMemorySaver pass.

## Tài liệu tham khảo chính thức

- [Persistence](./RESOURCES.md) — checkpoint, thread, history và fault tolerance.
- [Memory](./RESOURCES.md) — short-term memory, trimming và persistence.
- [LangGraph memory concepts](./RESOURCES.md) — thread/namespace và long-term memory overview.

## Nội dung tùy chọn nếu còn thời gian

Viết script dọn checkpoint hết retention trong môi trường development, nhưng chỉ sau khi có approval cho thao tác delete và không chạy trên dữ liệu thật.
