# Tháng 5 — Tuần 3: Human-in-the-loop và reliability boundary

## Mục tiêu tuần

Thêm một hành động nhạy cảm, `export_report`, vào research agent nhưng không cho nó tự chạy. Graph phải interrupt, lưu trạng thái, nhận approve/edit/reject, rồi resume an toàn với retry, timeout, tool budget, max steps và idempotency.

## Kiến thức cần đạt

- Human approval là checkpoint trong workflow, không thay authentication/authorization.
- Side effect phải xảy ra sau approval và có idempotency key; resume có thể chạy node lại.
- Retry chỉ áp dụng lỗi transient; timeout, tool budget và max steps là các giới hạn độc lập.

## Tính năng project sẽ bổ sung

`src/ai_assistant_platform/agents/approval.py`, `src/ai_assistant_platform/agents/tools.py`, policy reliability, route approve/resume và audit event append-only. Tool duy nhất có side effect trong tuần là export report giả lập vào storage adapter; không có delete/send email/ghi dữ liệu bên ngoài.

## Kế hoạch từng ngày

### Ngày 15 — Mô hình hóa hành động nhạy cảm và permission boundary

- **Mục tiêu cụ thể:** Chuyển yêu cầu export thành intent có dữ liệu đủ để người duyệt đánh giá.
- **Kết quả cần đạt:** `ExportReportIntent` có scope, format, reason, idempotency key; allowlist chỉ cho PDF/Markdown trong thư mục export của project.
- **Phân bổ thời gian:** 20 phút đọc, 45 phút schema/policy, 30 phút test, 10 phút ghi chú (105 phút).
- **Lý thuyết cần học:** Model không có quyền; application policy map tool/action sang permission và phạm vi dữ liệu cố định.
- **Tài liệu cần đọc:** Phần approve/edit/reject trong [Human-in-the-loop](./RESOURCES.md).
- **Bài thực hành:** Viết `can_request_export(state)`; từ chối path traversal, URL đích, format lạ và query chưa có citation.
- **Tích hợp project:** Thêm `export_report` như capability có schema, chưa đăng ký thực thi trực tiếp từ node draft.
- **File tạo/sửa:** `src/ai_assistant_platform/agents/policies.py`, `src/ai_assistant_platform/api/schemas/approval.py`, `tests/unit/test_export_policy.py`.
- **Lệnh chạy:** `uv run pytest tests/unit/test_export_policy.py -q`.
- **Kết quả mong đợi:** Fixture `../../secrets.txt` và export thiếu citation bị blocked trước khi đến tool.
- **Cách tự kiểm tra:** Assert lỗi client-safe, không phản chiếu absolute path hay internal policy detail.
- **Definition of Done:** Policy có allowlist, không dùng prompt text như nguồn quyền.
- **Commit message gợi ý:** `feat(agent): define export permission boundary`.
- **Câu hỏi tự kiểm tra:** Approval có làm path traversal an toàn không? Vì sao tool schema chưa đủ permission?

### Ngày 16 — Interrupt trước side effect

- **Mục tiêu cụ thể:** Pause graph khi export intent hợp lệ và hiển thị payload duyệt tối thiểu.
- **Kết quả cần đạt:** Graph trả trạng thái `interrupted` cùng approval ID/summary, không tạo file export.
- **Phân bổ thời gian:** 20 phút đọc, 50 phút graph/node, 25 phút test, 10 phút review (105 phút).
- **Lý thuyết cần học:** `interrupt()` tạm dừng execution và checkpoint state; code trước interrupt có thể chạy lại khi resume.
- **Tài liệu cần đọc:** Phần interrupts và side effects trong [Interrupts](./RESOURCES.md).
- **Bài thực hành:** Tạo node `request_export_approval`; dùng approval summary gồm citation IDs, format và reason, không đưa raw context.
- **Tích hợp project:** Nhánh `request_export` từ classify/draft đi tới interrupt thay vì gọi `ExportTool`.
- **File tạo/sửa:** `src/ai_assistant_platform/agents/approval.py`, `src/ai_assistant_platform/agents/graph.py`, `tests/integration/test_agent_interrupt.py`.
- **Lệnh chạy:** `uv run pytest tests/integration/test_agent_interrupt.py -q`.
- **Kết quả mong đợi:** `ExportTool.execute` mock có call count 0 khi graph interrupt.
- **Cách tự kiểm tra:** Chạy cùng thread một lần và inspect checkpoint: status pending, không có `export_receipt`.
- **Definition of Done:** Interrupt có checkpointer dependency và API không biến nó thành HTTP 500.
- **Commit message gợi ý:** `feat(agent): interrupt export for human approval`.
- **Câu hỏi tự kiểm tra:** Vì sao side effect không đặt trước interrupt? Người duyệt cần thấy thông tin nào là đủ?

### Ngày 17 — Approve, edit và reject để resume

- **Mục tiêu cụ thể:** Tạo contract quyết định người dùng và điều khiển resume có validation.
- **Kết quả cần đạt:** `POST /api/v1/agent/threads/{thread_id}/approval` chấp nhận `approve`, `edit`, `reject`; edit chỉ sửa format/reason allowlisted.
- **Phân bổ thời gian:** 15 phút ôn interrupt, 25 phút đọc, 50 phút API/service, 20 phút integration test (110 phút).
- **Lý thuyết cần học:** Resume payload là input không tin cậy; reject là outcome thành công, không phải exception.
- **Tài liệu cần đọc:** Ví dụ `Command(resume=...)` trong [Interrupts](./RESOURCES.md).
- **Bài thực hành:** Map action sang `Command(resume=decision)`; reject dẫn `finalize_cancelled`, edit revalidate intent rồi quay lại approval summary.
- **Tích hợp project:** Lưu audit event `approval_requested/decided` với actor pseudonymous và timestamp, không log content report.
- **File tạo/sửa:** `src/ai_assistant_platform/api/routes/agent.py`, `src/ai_assistant_platform/services/agent_approvals.py`, `tests/integration/test_agent_approval_api.py`.
- **Lệnh chạy:** `uv run pytest tests/integration/test_agent_approval_api.py -q`.
- **Kết quả mong đợi:** Ba fixture approve/edit/reject đều có status rõ; reject không gọi tool.
- **Cách tự kiểm tra:** Gửi action lạ/edit destination path và assert 422/blocked; xem audit không chứa secret.
- **Definition of Done:** Mỗi decision gắn đúng pending approval/thread và không resume nhầm checkpoint.
- **Commit message gợi ý:** `feat(agent): add validated approval resume actions`.
- **Câu hỏi tự kiểm tra:** Edit khác approve như thế nào? Vì sao reject không nên trả 500?

### Ngày 18 — Idempotent export và audit receipt

- **Mục tiêu cụ thể:** Đảm bảo resume/retry không tạo nhiều export cho cùng intent.
- **Kết quả cần đạt:** Tool dùng idempotency key; gọi hai lần trả cùng receipt, chỉ ghi artifact một lần trong fake storage.
- **Phân bổ thời gian:** 20 phút đọc, 45 phút adapter, 30 phút unit test, 15 phút note (110 phút).
- **Lý thuyết cần học:** Idempotency bảo vệ khỏi duplicate do retry, resume hay client re-send; key cần gắn semantic intent, không chỉ request UUID.
- **Tài liệu cần đọc:** Lưu ý idempotency quanh side effect trong [Interrupts](./RESOURCES.md).
- **Bài thực hành:** Tạo `ExportStore.put_if_absent`; receipt gồm export ID/status/hash, không trả local path nội bộ.
- **Tích hợp project:** Node thực thi chỉ chạy khi approval approved và gọi tool qua adapter interface.
- **File tạo/sửa:** `src/ai_assistant_platform/agents/tools.py`, `src/ai_assistant_platform/services/export_store.py`, `tests/unit/test_export_idempotency.py`.
- **Lệnh chạy:** `uv run pytest tests/unit/test_export_idempotency.py -q`.
- **Kết quả mong đợi:** Same key có one write; key khác cùng content là event khác theo policy.
- **Cách tự kiểm tra:** Assert receipt equality/call count, sau đó simulate exception sau write để kiểm tra recover path.
- **Definition of Done:** Không có file system write trực tiếp trong graph node và audit receipt không chứa report raw.
- **Commit message gợi ý:** `feat(agent): make approved exports idempotent`.
- **Câu hỏi tự kiểm tra:** Khi nào cùng content không nên dùng chung key? Idempotency thay transaction được không?

### Ngày 19 — Timeout và retry phân loại lỗi

- **Mục tiêu cụ thể:** Bọc retrieval/export tool bằng timeout và retry policy hữu hạn.
- **Kết quả cần đạt:** Transient timeout/503 retry tối đa 2 lần với backoff testable; validation/permission error không retry.
- **Phân bổ thời gian:** 20 phút đọc, 45 phút policy/wrapper, 30 phút tests, 15 phút review (110 phút).
- **Lý thuyết cần học:** Timeout là deadline; retry tăng tải nên cần giới hạn, phân loại error và jitter/backoff. Không retry side effect nếu không có idempotency.
- **Tài liệu cần đọc:** Phần durable execution/retry awareness trong [Persistence](./RESOURCES.md).
- **Bài thực hành:** Tạo `ToolExecutionPolicy(timeout_seconds=5, max_attempts=2)`; inject clock/sleep fake trong test.
- **Tích hợp project:** `rag_search` vẫn read-only; `export_report` chỉ được retry sau khi Ngày 18 đã có idempotency key.
- **File tạo/sửa:** `src/ai_assistant_platform/agents/reliability.py`, `src/ai_assistant_platform/agents/tools.py`, `tests/unit/test_tool_retry_timeout.py`.
- **Lệnh chạy:** `uv run pytest tests/unit/test_tool_retry_timeout.py -q`.
- **Kết quả mong đợi:** Transient fixture gọi 2 lần rồi success/failure; invalid input gọi đúng một lần.
- **Cách tự kiểm tra:** Assert elapsed deadline, attempts metadata và error sanitized; không dùng `sleep` thật trong unit test.
- **Definition of Done:** Retry policy không bắt mọi `Exception` và có metric/audit field cho attempt count.
- **Commit message gợi ý:** `feat(agent): bound tool retries and timeouts`.
- **Câu hỏi tự kiểm tra:** Timeout khác cancellation thế nào? Vì sao retry validation error gây hại?

### Ngày 20 — Milestone: max steps, tool budget và error recovery

- **Mục tiêu cụ thể:** Đặt budget cho toàn graph và kiểm tra mọi failure dừng an toàn.
- **Kết quả cần đạt:** Graph dừng khi quá 6 steps hoặc 2 tool calls; timeout/approval stale đưa state tới `failed_safe`/`cancelled`, không loop.
- **Phân bổ thời gian:** 20 phút thiết kế case, 50 phút implement/test, 30 phút integration smoke, 15 phút document (115 phút).
- **Lý thuyết cần học:** Step limit chống loop orchestration; tool budget chống cost/side effect. Chúng đo khác nhau và phải kiểm trước tool call.
- **Tài liệu cần đọc:** Xem lại graph routing trong [Graph API overview](./RESOURCES.md) và interrupt lifecycle trong [Interrupts](./RESOURCES.md).
- **Bài thực hành:** Thêm `enforce_limits` node/conditional edge; fixture loop route, budget exhausted, stale approval và tool timeout.
- **Tích hợp project:** API response có `status`, `stop_reason`, `step_count`, `tool_calls_used`; không trả stack trace.
- **File tạo/sửa:** `src/ai_assistant_platform/agents/policies.py`, `src/ai_assistant_platform/agents/graph.py`, `tests/integration/test_agent_reliability.py`, `docs/agent-reliability.md`.
- **Lệnh chạy:** `uv run pytest tests/integration/test_agent_reliability.py -q`; `uv run pytest tests/unit/test_tool_retry_timeout.py -q`.
- **Kết quả mong đợi:** Mỗi failure fixture kết thúc trong giới hạn và export chỉ có receipt khi approved.
- **Cách tự kiểm tra:** Assert graph `step_count <= 6`, mock tool calls `<= 2`, và state terminal cho từng case.
- **Definition of Done:** Limit/budget là Settings có test boundary (`limit-1`, `limit`, `limit+1`).
- **Commit message gợi ý:** `feat(agent): enforce workflow and tool execution budgets`.
- **Câu hỏi tự kiểm tra:** Max steps có thay tool budget không? Error recovery nào cần người dùng bắt đầu request mới?

### Ngày 21 — Review/buffer: diễn tập approval an toàn

- **Mục tiêu cụ thể:** Chạy một scenario từ request export đến approve/reject và ghi handoff guardrail.
- **Kết quả cần đạt:** Demo có một approval thành công, một reject, một timeout; audit timeline không chứa report/secret.
- **Phân bổ thời gian:** 15 phút chuẩn bị, 35 phút scenario, 25 phút suite, 15 phút audit review (90 phút).
- **Lý thuyết cần học:** HITL đáng tin khi quyết định có context vừa đủ, state durable và outcome truy vết được.
- **Tài liệu cần đọc:** Đọc lại [Human-in-the-loop](./RESOURCES.md), tập trung approve/edit/reject.
- **Bài thực hành:** Viết sequence diagram và update handoff; refactor một duplicated policy nếu test vẫn rõ.
- **Tích hợp project:** Tạo `docs/month-05-week-03-handoff.md` liệt kê sensitive boundary, retry/budget, audit event và contract cho guardrail tuần 4.
- **File tạo/sửa:** `docs/architecture/agent-workflow.md`, `docs/month-05-week-03-handoff.md`, `tests/integration/test_agent_approval_api.py`.
- **Lệnh chạy:** `uv run pytest tests/integration/test_agent_interrupt.py tests/integration/test_agent_approval_api.py tests/integration/test_agent_reliability.py -q`; `uv run ruff check .`.
- **Kết quả mong đợi:** Scenario pass, audit only has structured metadata, no action tự động vượt approval.
- **Cách tự kiểm tra:** Đọc diagram từ trái sang phải và chỉ ra checkpoint nào tồn tại trước/ sau side effect.
- **Definition of Done:** Có thể chỉ ra bằng test rằng approve/edit/reject, duplicate resume và timeout đều có đường kết thúc.
- **Commit message gợi ý:** `docs(agent): review approval and reliability handoff`.
- **Câu hỏi tự kiểm tra:** Approval log cần đủ gì để audit? Node nào phải idempotent khi resume?

## Milestone cuối tuần

Export report bị pause trước side effect, có approve/edit/reject, durable audit metadata, idempotency, retry/timeout có giới hạn và graph không vượt max steps/tool budget.

## Review checklist

- [ ] Intent/tool có allowlist và citation boundary trước approval.
- [ ] Interrupt xảy ra trước file write; reject không chạy tool.
- [ ] Resume validate payload và gắn đúng pending thread/approval.
- [ ] Side effect idempotent, receipt/audit đã redact.
- [ ] Retry chỉ transient, timeout và attempts có giới hạn.
- [ ] Max steps/tool budget có test giới hạn và terminal error an toàn.

## Definition of Done

Hoàn thành bảy ngày với integration test interrupt/resume và unit test policy/tool; không có destructive tool hoặc bypass approval; handoff cung cấp contract reliability cho Tuần 4.

## Lỗi thường gặp

- Hiển thị raw prompt/context cho người duyệt thay vì summary tối thiểu.
- Gọi tool trước interrupt hoặc retry write không idempotent.
- Coi approval là authentication và bỏ qua permission policy.
- Chỉ dùng max steps rồi quên giới hạn tool/cost.

## Tài liệu tham khảo chính thức

- [Interrupts](./RESOURCES.md) — pause/resume và idempotency.
- [Human-in-the-loop](./RESOURCES.md) — approve, edit, reject.
- [Persistence](./RESOURCES.md) — checkpoint/durable execution.

## Nội dung tùy chọn nếu còn thời gian

Thêm expiry UI cho approval pending bằng một job mock; không thêm email, browser tool hay thông báo ra hệ thống bên ngoài.
