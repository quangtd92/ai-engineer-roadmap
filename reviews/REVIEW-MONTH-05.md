# Month 05 Review

## Status

PASS_WITH_NOTES

## Scope

Review curriculum Month-05: README, bốn tuần (28 ngày), tài liệu tham khảo và các liên kết nội bộ do Month-05 sử dụng. Không sửa hay đánh giá nội dung Month-06 ngoài việc xác nhận cầu nối/handoff không làm thay đổi file Month-06.

## Files reviewed

- `Month-05/README.md`
- `Month-05/Week-01.md` đến `Month-05/Week-04.md`
- `Month-05/RESOURCES.md`
- `Month-04/README.md`, `Month-04/Week-04.md` (đầu vào RAG/evaluation)
- `Month-06/README.md`, `Month-06/Week-01.md` (cầu nối, chỉ đọc)
- `ROADMAP_SPEC.md`, `VALIDATION.md`, `IMPLEMENTATION_PLAN.md`

## Deliverables verified

- Workflow LangGraph xác định: typed state, node/edge, conditional route, citation review và API contract (Tuần 1).
- Checkpoint theo `thread_id`, short-term memory có giới hạn, history redact và persistence adapter/contract test (Tuần 2).
- Human approval interrupt/resume, approve/edit/reject, idempotent export, timeout/retry/max steps/tool budget (Tuần 3).
- Guardrail, least-privilege matrix, tracing LangSmith opt-in/redaction, agent dataset, baseline/threshold/report và handoff Month-06 (Tuần 4).

## Validation summary

### Repository structure

PASS — Month-05 có README, `Week-01.md`–`Week-04.md` và `RESOURCES.md`; báo cáo review đặt tại repository root theo convention `REVIEW-MONTH-01.md`–`REVIEW-MONTH-04.md` hiện có.

### Daily completeness

PASS — Có 28 ngày. Mỗi ngày có mục tiêu, kết quả, thời lượng, lý thuyết, tài liệu, thực hành, tích hợp project, file, lệnh, expected result, verification, DoD, commit message và 2 câu hỏi tự kiểm tra. Week-02–04 không còn template; Week-01 đã có cùng cấu trúc chi tiết.

### Time budget

PASS — Mọi ngày nằm trong 90–120 phút; milestone không quá 120 phút và ngày 7/14/21/28 là review/buffer 90 phút. Không ngày nào yêu cầu đồng thời xây feature lớn, deploy cloud và evaluation LLM bắt buộc.

### Technical sequence

PASS — Tuần 1 dùng RAG read-only/citation từ Month-04 để tạo deterministic graph; Tuần 2 checkpoint state đó; Tuần 3 thêm interrupt trước side effect; Tuần 4 mới thêm policy, tracing và evaluation. Month-06 chỉ nhận handoff configuration/quality contract, không bị thay đổi.

### Project progression

PASS — Mọi bài tập mở rộng cùng `ai-assistant-platform`: `src/ai_assistant_platform/agents`, API agent, checkpoint service, export adapter, guardrails, observability và `evals/agent`. Không có mini-project độc lập.

### References and internal links

PASS — Link tuần trỏ tới `RESOURCES.md`; resource file dùng HTTPS và ghi phần cần đọc. Đã kiểm tra các target nội bộ Month-04/05/06 được liên kết trong Month-05 và target đều tồn tại. Mỗi tuần có tối đa bốn nguồn bắt buộc.

### Security and reliability

PASS — Không yêu cầu secret thật/hard-code credential; `.env.example` chỉ chứa tên biến. Có input/output validation, prompt-injection awareness, permission matrix, approval cho export, bounded retry/timeout, max steps/tool budget, idempotency và redaction tracing.

### Evaluation

PASS — Dataset versioned, expected behavior, deterministic baseline/threshold, regression tests, optional DeepEval, latency/cost signal, failure taxonomy và report. Không coi một LLM-as-judge metric là kết luận duy nhất.

## Issues found

1. Week-02, Week-03 và Week-04 ban đầu chỉ là template tiếng Anh, không có các trường bắt buộc cấp ngày.
2. README Month-05 thiếu phần điều hướng/review rõ ràng và dùng format thời lượng `60--120`.
3. Cần làm rõ rằng persistence durable và DeepEval có prerequisite external, không được báo pass giả khi thiếu Postgres/credential.

## Issues fixed

1. Thay thế toàn bộ 21 ngày template bằng kế hoạch cụ thể 90–115 phút/ngày, có command/test/DoD/câu hỏi riêng.
2. Hoàn thiện README với điều hướng tuần, link review và format nhất quán.
3. Ghi rõ contract test offline vs integration Postgres, `skipped_missing_credentials` cho evaluator và không đưa secret vào Git.

## Open issues

- Đây là review của curriculum, không phải bằng chứng source code `ai-assistant-platform` đã được người học triển khai. Các lệnh là acceptance checks phải chạy khi thực hiện roadmap.
- Persistence PostgreSQL, LangSmith và DeepEval cần dependency/credential hợp lệ; tài liệu yêu cầu báo `skip` có chủ đích thay vì giả định pass.

## Recommendation for Month-06

Đóng gói đúng graph/persistence contract này: readiness kiểm tra dependency bắt buộc, CI chạy deterministic agent regression không cần secret, trace giữ redaction/sampling và deployment không tự migrate hoặc auto-resume side effect chưa được approval.
