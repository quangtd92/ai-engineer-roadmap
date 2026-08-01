# Tháng 5 — Tuần 4: Guardrails, tracing và agent evaluation

## Mục tiêu tuần

Đưa reliability của Tuần 3 thành quality gate có thể quan sát và đánh giá. Tuần này thêm guardrail input/output, prompt-injection defense, LangSmith tracing opt-in, dataset agent evaluation, baseline/threshold và failure taxonomy; không thêm framework agent mới.

## Kiến thức cần đạt

- Guardrail là nhiều lớp validation/policy, không phải một system prompt duy nhất.
- Trace phục vụ debug/evaluation khi có metadata tối thiểu và redaction; không phải nơi lưu secret hay raw PII.
- Agent evaluation kết hợp assertion xác định với metric tool correctness/task completion, latency/cost và review lỗi.

## Tính năng project sẽ bổ sung

`app/agents/guardrails.py`, redacted trace adapter, `evals/agent/` với dataset/runner/report, threshold config và `docs/month-06-handoff.md`. RAG và approval contracts của các tuần trước được tái sử dụng, không copy retrieval/tool code.

## Kế hoạch từng ngày

### Ngày 22 — Input guardrail và prompt-injection policy

- **Mục tiêu cụ thể:** Chặn input không phù hợp trước khi graph tốn retrieval/tool budget.
- **Kết quả cần đạt:** Guardrail validate length, required query, export intent và pattern injection rõ ràng; case nghi ngờ được `blocked_input` có request ID.
- **Phân bổ thời gian:** 20 phút đọc, 45 phút code, 30 phút test, 10 phút ghi chú (105 phút).
- **Lý thuyết cần học:** Prompt injection là input không tin cậy; detect pattern chỉ là defense-in-depth, permission/citation/tool boundary vẫn bắt buộc.
- **Tài liệu cần đọc:** Phần security boundary trong [LangGraph overview](./RESOURCES.md) và xem lại handoff RAG Month-04.
- **Bài thực hành:** Viết `validate_agent_input`; từ chối query vượt 2,000 ký tự, control character và yêu cầu “bỏ qua policy/đọc secret” theo policy minh bạch.
- **Tích hợp project:** Agent route gọi guardrail trước `classify`; blocked request không tạo export/LLM/tool call.
- **File tạo/sửa:** `app/agents/guardrails.py`, `app/api/routes/agent.py`, `tests/unit/test_agent_input_guardrail.py`.
- **Lệnh chạy:** `uv run pytest tests/unit/test_agent_input_guardrail.py -q`.
- **Kết quả mong đợi:** Benign research query pass; injection/oversize fixtures block với message không tiết lộ rule chi tiết.
- **Cách tự kiểm tra:** Assert `retriever`/`export_tool` mock call count bằng 0 khi input bị block.
- **Definition of Done:** Guardrail có false-positive note và không tuyên bố regex giải quyết toàn bộ injection.
- **Commit message gợi ý:** `feat(agent): validate unsafe and oversized inputs`.
- **Câu hỏi tự kiểm tra:** Vì sao prompt filter không thay permission boundary? False positive xử lý ở đâu?

### Ngày 23 — Output guardrail và citation/approval invariants

- **Mục tiêu cụ thể:** Kiểm tra kết quả trước khi trả API response hoặc ghi export receipt.
- **Kết quả cần đạt:** Nhánh RAG chỉ final khi citations tồn tại trong retrieved IDs; export receipt chỉ final sau approval; answer vượt limit bị truncated/block theo policy.
- **Phân bổ thời gian:** 15 phút ôn contracts, 25 phút đọc, 50 phút validator/test, 20 phút review (110 phút).
- **Lý thuyết cần học:** Output validation xác nhận invariant xác định; LLM judge hữu ích sau đó nhưng không thay validation schema/citation.
- **Tài liệu cần đọc:** Phần graph state/nodes trong [Graph API overview](./RESOURCES.md).
- **Bài thực hành:** Viết `validate_agent_output(state)` và response Pydantic model; map failure sang `blocked_output` không lộ draft nội bộ.
- **Tích hợp project:** Review node Tuần 1 gọi validator này sau draft và sau approved export; direct answer không được gắn citation giả.
- **File tạo/sửa:** `app/agents/guardrails.py`, `app/agents/nodes.py`, `tests/unit/test_agent_output_guardrail.py`.
- **Lệnh chạy:** `uv run pytest tests/unit/test_agent_output_guardrail.py -q`.
- **Kết quả mong đợi:** Missing/foreign citation, unapproved receipt và answer oversize đi vào failure path xác định.
- **Cách tự kiểm tra:** Fixture citation ID lạ phải fail dù URL trông hợp lệ; assert API không trả `draft`.
- **Definition of Done:** Validation tái sử dụng document IDs/approval status có thẩm quyền, không tin string model tạo.
- **Commit message gợi ý:** `feat(agent): enforce output citation and approval invariants`.
- **Câu hỏi tự kiểm tra:** Output validation khác prompt instruction thế nào? Vì sao direct answer không có citation mặc định?

### Ngày 24 — Permission matrix và negative-path tests

- **Mục tiêu cụ thể:** Làm policy boundary có thể review thay vì rải `if` trong node.
- **Kết quả cần đạt:** Matrix xác định route nào được RAG read-only, route nào có thể request export, route nào bị deny; test deny-by-default.
- **Phân bổ thời gian:** 20 phút đọc/thiết kế, 45 phút policy refactor, 30 phút tests, 15 phút ADR (110 phút).
- **Lý thuyết cần học:** Least privilege bắt đầu bằng deny default; tool parameters cũng là boundary, không chỉ tool name.
- **Tài liệu cần đọc:** Phần tools/security concepts trong [Workflows and agents](./RESOURCES.md).
- **Bài thực hành:** Tạo `AgentPermission` enum/matrix; test tool unknown, export without citation, write outside allowlist và re-run rejected approval.
- **Tích hợp project:** `classify`/`request_approval` hỏi cùng policy module; graph không import storage implementation trực tiếp.
- **File tạo/sửa:** `app/agents/policies.py`, `docs/adr/007-agent-permission-matrix.md`, `tests/unit/test_agent_permissions.py`.
- **Lệnh chạy:** `uv run pytest tests/unit/test_agent_permissions.py -q`; `uv run ruff check app/agents`.
- **Kết quả mong đợi:** Tất cả capability không khai báo bị deny, error return có code ổn định cho client.
- **Cách tự kiểm tra:** Thêm fake tool trong fixture và xác nhận test đỏ trước khi policy explicit cho phép.
- **Definition of Done:** Matrix phân biệt read-only retrieval với export side effect và liên kết approval policy Tuần 3.
- **Commit message gợi ý:** `refactor(agent): centralize least-privilege tool policy`.
- **Câu hỏi tự kiểm tra:** Allowlist parameter quan trọng khi nào? Một tool read-only còn cần timeout/budget không?

### Ngày 25 — LangSmith tracing opt-in và redaction

- **Mục tiêu cụ thể:** Tạo trace liên kết với request/checkpoint mà không phát tán dữ liệu nhạy cảm.
- **Kết quả cần đạt:** Trace enable bằng Settings; metadata gồm hashed thread ID, route, step/tool count, latency, status; raw authorization/secret bị redact.
- **Phân bổ thời gian:** 20 phút đọc, 45 phút adapter/settings, 30 phút unit test, 15 phút config review (110 phút).
- **Lý thuyết cần học:** Trace giúp quan sát execution path; sampling/redaction giảm privacy risk và cost. Tracing off phải không làm workflow fail.
- **Tài liệu cần đọc:** Phần LangSmith integration trong [LangGraph overview](./RESOURCES.md).
- **Bài thực hành:** Viết `TraceContext`/wrapper không phụ thuộc global env trong test; thêm `LANGSMITH_TRACING` và tên project rỗng vào `.env.example`, không thêm key.
- **Tích hợp project:** `AgentService` tạo run metadata từ state terminal, gắn `request_id` của API nhưng không gửi message/document raw mặc định.
- **File tạo/sửa:** `app/observability/langsmith.py`, `app/core/settings.py`, `.env.example`, `tests/unit/test_agent_tracing.py`.
- **Lệnh chạy:** `uv run pytest tests/unit/test_agent_tracing.py -q`.
- **Kết quả mong đợi:** Disabled config là no-op; enabled fixture nhận redacted metadata; log/test không chứa `LANGSMITH_API_KEY`.
- **Cách tự kiểm tra:** `rg -n "LANGSMITH_API_KEY=.*[^\s]" .env.example` không có giá trị; assert `thread_id` plaintext vắng trong emitted metadata.
- **Definition of Done:** Có test trace disabled/enabled/redaction và tài liệu ghi trace project/key là prerequisite external.
- **Commit message gợi ý:** `feat(observability): add opt-in redacted agent tracing`.
- **Câu hỏi tự kiểm tra:** Vì sao hash thread ID vẫn cần được bảo vệ? Trace có thể thay audit log không?

### Ngày 26 — Dataset agent evaluation và baseline xác định

- **Mục tiêu cụ thể:** Version hóa case đánh giá end-to-end trước khi gọi LLM judge.
- **Kết quả cần đạt:** JSONL 10–12 case có expected route, tool calls, approval outcome, citation expectation, category và no-action cases; runner deterministic ghi baseline.
- **Phân bổ thời gian:** 20 phút đọc, 45 phút dataset/runner, 30 phút schema tests, 15 phút baseline note (110 phút).
- **Lý thuyết cần học:** Agent eval cần trace/expected behavior; route/budget/permission assertions là deterministic test, khác score quality của answer.
- **Tài liệu cần đọc:** [DeepEval agent evaluation quickstart](./RESOURCES.md) — trace và component/end-to-end evaluation.
- **Bài thực hành:** Tạo fixture research, direct, injection, missing citation, export approve/reject, timeout, budget exhaustion; record dataset version and executor config.
- **Tích hợp project:** `run_agent_eval.py --mode deterministic` gọi graph fake dependencies, không cần OpenAI/LangSmith credential.
- **File tạo/sửa:** `evals/agent/dataset.jsonl`, `evals/agent/schema.py`, `evals/agent/run_agent_eval.py`, `tests/evaluation/test_agent_dataset.py`.
- **Lệnh chạy:** `uv run pytest tests/evaluation/test_agent_dataset.py -q`; `uv run python evals/agent/run_agent_eval.py --mode deterministic`.
- **Kết quả mong đợi:** Report JSON có pass rate route/tool/approval, p50 latency fake và per-case failure; no-action cases không gọi export.
- **Cách tự kiểm tra:** Dataset validator reject duplicate ID/missing expectation; fixture sai route làm runner exit non-zero.
- **Definition of Done:** Dataset do người viết/review, không sinh bằng model đang đánh giá; baseline ghi rõ scope không phải benchmark công khai.
- **Commit message gợi ý:** `test(agent): add versioned deterministic evaluation dataset`.
- **Câu hỏi tự kiểm tra:** Unit test và evaluation dataset khác nhau thế nào? No-action case chứng minh rủi ro nào?

### Ngày 27 — DeepEval optional, threshold và failure taxonomy

- **Mục tiêu cụ thể:** Bổ sung tín hiệu evaluator cho trace mà không để LLM judge chặn CI.
- **Kết quả cần đạt:** Optional runner DeepEval đo Tool Correctness và Task Completion trên 3–5 trace; deterministic threshold và taxonomy có report trước/sau.
- **Phân bổ thời gian:** 25 phút đọc, 35 phút adapter, 30 phút run/report, 20 phút error analysis (110 phút).
- **Lý thuyết cần học:** Tool correctness đánh giá tool/args mong đợi; task completion nhìn outcome trace. Cả hai có variance/cost và không thay manual review/safety assertions.
- **Tài liệu cần đọc:** [DeepEval tool correctness](./RESOURCES.md) và [DeepEval task completion](./RESOURCES.md).
- **Bài thực hành:** Thêm `--mode deepeval` trả `skipped_missing_credentials` khi thiếu provider key; đặt deterministic thresholds ví dụ route pass >= 0.90, unauthorized export = 0, tool calls <= 2.
- **Tích hợp project:** Viết `evals/agent/reports/month-05.md` gồm baseline/current, latency/cost nếu available, categories routing/retrieval/approval/guardrail/tool/retry/evaluator.
- **File tạo/sửa:** `evals/agent/deepeval_adapter.py`, `evals/agent/thresholds.py`, `evals/agent/reports/month-05.md`, `tests/evaluation/test_agent_regression.py`.
- **Lệnh chạy:** `uv run pytest tests/evaluation/test_agent_regression.py -q`; `uv run python evals/agent/run_agent_eval.py --mode deepeval --subset smoke`.
- **Kết quả mong đợi:** Offline regression pass/fail ổn định; optional evaluator tạo report hoặc skip chủ đích, không in credential.
- **Cách tự kiểm tra:** Cố ý sửa expected tool trong local fixture để thấy failure case ID; xác nhận report không suy ra kết luận từ một metric.
- **Definition of Done:** Report có baseline, nhiều metric, threshold, per-case failure và next action có giới hạn.
- **Commit message gợi ý:** `test(agent): add agent quality gate and failure analysis`.
- **Câu hỏi tự kiểm tra:** Tool correctness không đo điều gì? Vì sao missing credential là skip chứ không pass?

### Ngày 28 — Milestone: regression run, review và handoff production

- **Mục tiêu cụ thể:** Chạy agent demo/evaluation có evidence và chuẩn bị đúng input cho Month-06.
- **Kết quả cần đạt:** End-to-end fake demo cho direct/RAG/blocked/export approval; suite, report và handoff nêu config/health/evaluation command/tracing sampling.
- **Phân bổ thời gian:** 15 phút chuẩn bị, 40 phút demo+eval, 25 phút test/lint, 20 phút review/handoff (100 phút).
- **Lý thuyết cần học:** Production handoff là contract vận hành: dependencies, boundaries, health/evaluation signals và known limitations; không phải lời hứa deploy xong.
- **Tài liệu cần đọc:** Xem lại [DeepEval agent evaluation quickstart](./RESOURCES.md) và các handoff Tuần 1–3.
- **Bài thực hành:** Viết `docs/month-06-handoff.md` có env variable names, Postgres/Redis/Qdrant readiness dependency, migration/checkpoint note, test/eval commands, trace redaction/sampling và rollback-safe limitation.
- **Tích hợp project:** Thêm `docs/agent-demo.md`; API demo không gửi real export, dùng fake storage/test fixture; cập nhật README project khi tồn tại.
- **File tạo/sửa:** `docs/month-06-handoff.md`, `docs/agent-demo.md`, `tests/integration/test_agent_e2e.py`, `evals/agent/reports/month-05.md`.
- **Lệnh chạy:** `uv run pytest tests/unit/test_agent_input_guardrail.py tests/unit/test_agent_output_guardrail.py tests/evaluation/test_agent_regression.py tests/integration/test_agent_e2e.py -q`; `uv run ruff check .`.
- **Kết quả mong đợi:** Four scenario results có status/citation/approval đúng; report nêu failures/limitations; Month-06 không bị sửa.
- **Cách tự kiểm tra:** Kiểm tra link handoff từ README Month-05, chạy `rg -n "sk-|API_KEY=.+" docs evals .env.example` và xác nhận không có secret.
- **Definition of Done:** Handoff đủ để Month-06 đóng gói/monitor mà không cần đọc internal state; không tạo cloud resource hoặc thay đổi file Month-06.
- **Commit message gợi ý:** `docs(agent): publish evaluated workflow handoff for production`.
- **Câu hỏi tự kiểm tra:** Quality gate nào chạy offline? Month-06 cần biết dependency nào để readiness? Vì sao demo fake export vẫn hữu ích?

## Milestone cuối tuần

Agent chặn input/output sai policy, dùng permission matrix, trace opt-in đã redact, có dataset + regression baseline/threshold + failure report, và handoff chính xác sang Month-06.

## Review checklist

- [ ] Input/output guardrail có negative-path tests và không hứa chặn mọi injection.
- [ ] Citation, approval và tool policy dùng nguồn dữ liệu có thẩm quyền.
- [ ] Trace bật/tắt được, metadata tối thiểu và đã redact.
- [ ] Dataset có route/tool/approval/no-action case; deterministic runner không cần secret.
- [ ] DeepEval là lớp optional; report có metric đa chiều, threshold và taxonomy.
- [ ] Handoff ghi dependencies/config/commands/known limitations mà không sửa Month-06.

## Definition of Done

Hoàn thành bảy ngày; guardrail, trace và agent evaluation có code/test/report riêng; regression phát hiện route/tool/permission regression; sản phẩm có handoff production an toàn.

## Lỗi thường gặp

- Tin một regex hoặc system prompt sẽ chặn mọi prompt injection.
- Trace toàn bộ prompt/document/authorization để “debug cho tiện”.
- Dùng LLM judge làm test CI bắt buộc rồi không xử lý variance/credential.
- Chỉ đo answer hay mà bỏ qua tool sai, export trái phép hoặc budget vượt limit.

## Tài liệu tham khảo chính thức

- [LangGraph overview](./RESOURCES.md) — orchestration và tracing integration.
- [DeepEval agent evaluation quickstart](./RESOURCES.md) — trace/component/end-to-end evaluation.
- [DeepEval tool correctness](./RESOURCES.md) — expected tool và threshold.
- [DeepEval task completion](./RESOURCES.md) — outcome full trace.

## Nội dung tùy chọn nếu còn thời gian

Thử trace sampling 10% trên fixture local hoặc thêm one-page dashboard từ report JSON. Không thêm multi-agent, browser automation hay framework guardrail thứ hai.
