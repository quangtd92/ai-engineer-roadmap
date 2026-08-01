# Review Month 03

## Status

PASS_WITH_NOTES

**Ngày tự review:** 2026-08-01. Review này được chạy lại sau khi bổ sung mục **Tài liệu** riêng cho cả 28 ngày học.

## Scope

Review nội dung curriculum của Month-03: LLM Engineering, Structured Output, Tool Calling và MCP. Đây là review tài liệu; không xác nhận source code project hay API credential thật vì repository hiện không chứa `ai-assistant-platform`.

## Files reviewed

- `Month-03/README.md`
- `Month-03/Week-01.md`
- `Month-03/Week-02.md`
- `Month-03/Week-03.md`
- `Month-03/Week-04.md`
- `VALIDATION.md`, `ROADMAP_SPEC.md`, `IMPLEMENTATION_PLAN.md`
- Điểm tiếp nối: `Month-02/Week-04.md`, `Month-04/Week-01.md` và README tháng liền kề (chỉ đọc, không sửa).

## Deliverables verified

- [x] Contract adapter OpenAI Responses API, chat thường và SSE streaming.
- [x] Config an toàn, timeout, retry bị giới hạn và telemetry usage/latency/error.
- [x] Structured Output với Pydantic validation và fallback.
- [x] Prompt regression dataset, baseline, metric và failure report.
- [x] Hai tool deterministic, read-only; schema, timeout, retry, budget và max iteration.
- [x] MCP server local có tool, resource, discovery, audit và negative tests.
- [x] Handoff cụ thể sang retrieval/citation của Month 04.

## Validation summary

### Repository structure

PASS_WITH_NOTES — Năm file được yêu cầu tồn tại và các link nội bộ từ README đến bốn tuần/review dùng đường dẫn tương đối hợp lệ. Repository vẫn thiếu project code thực, và các tháng khác còn thiếu `REVIEW.md`/`RESOURCES.md`; nằm ngoài phạm vi chỉnh sửa này.

### Daily completeness

PASS — Có 28 ngày (01–28). Mỗi ngày có mục tiêu, kết quả, thời lượng, lý thuyết/tài liệu, thực hành, tích hợp project, file, lệnh, expected result, kiểm tra, DoD, commit và hai câu hỏi. Trọng tâm lần lượt tăng từ adapter đến MCP, không dùng cùng nội dung ngày.

### Time budget

PASS — Mỗi ngày ghi 85–115 phút; milestone Day 07, 21, 27 và 28 không vượt 120 phút. API smoke test thật được đánh dấu tùy chọn để không biến API key/quota thành điều kiện hoàn thành.

### Technical sequence

PASS_WITH_NOTES — Tuần 01 thiết lập adapter/error/stream trước Structured Output; Tuần 02 tạo schema/evaluation trước tool use; Tuần 03 giới hạn tool loop trước MCP; Tuần 04 dùng lại capability rồi bàn giao RAG. Month-02 hiện là template nên prerequisite được ghi thành giả định rõ ràng thay vì tuyên bố người học đã có file cụ thể.

### Project progression

PASS — Mỗi ngày có thay đổi xác định cho `ai-assistant-platform`; route không bị trộn provider logic, tool docs catalog được ghi rõ là baseline sẽ thay bằng RAG, không phải RAG giả.

### References and links

PASS — Tài liệu tham khảo dùng OpenAI, FastAPI, Pydantic và MCP official documentation; tuần link về README tháng hoặc nguồn MCP trực tiếp. Đã kiểm tra link nội bộ bằng script Markdown ở phần kiểm tra kỹ thuật bên dưới.

### Security

PASS — Không hard-code key; `.env.example`, redaction, model allowlist, input validation, timeout/retry bounded, read-only tool boundary, audit log và injection test case đều được dạy đúng thời điểm. Human approval cho hành động nhạy cảm không áp dụng cho Month 03 vì capability bắt buộc không có side effect; Month 05 sẽ là nơi áp dụng workflow approval.

### Evaluation

PASS — Có prompt regression test data, baseline, pass rate, schema-valid rate, fallback count, failure taxonomy và exit code. Tài liệu phân biệt unit/integration test với evaluation, và không kết luận chất lượng chỉ từ một metric.

## Technical checks performed

- [x] Có đúng 28 heading `### Ngày`; mọi entry đều có đủ 14 trường bắt buộc, gồm mục **Tài liệu** riêng.
- [x] Thời lượng thấp nhất/cao nhất là 85/115 phút; không ngày nào vượt 120 phút.
- [x] Script kiểm tra Markdown relative link báo `relative_link_issues=0`.
- [x] Tìm placeholder bằng `rg` không có kết quả; lệnh trả exit code 1 vì không tìm thấy chuỗi, đây là kết quả mong đợi.
- [x] Đối chiếu thủ công các nguồn OpenAI và MCP chính thức được dùng trong Month-03; các link OpenAI cũ chuyển hướng sang `developers.openai.com` hợp lệ.
- [x] Không sửa file trong `Month-04`, `Month-05` hoặc `Month-06`.

## Issues found

1. Month-02 và Month-04 vẫn là template, nên không thể xác minh thực tế các file/code prerequisite hoặc handoff bằng curriculum chi tiết.
2. Repository hiện không phải Git repository và chưa có source code `ai-assistant-platform`; các command là contract học tập để áp dụng khi project được tạo ở Month 01.
3. Báo giá và model availability không được chốt trong tài liệu, vì thay đổi theo thời điểm/tài khoản.

## Issues fixed

- Thay toàn bộ template Month-03 bằng kế hoạch tiếng Việt, 28 ngày riêng biệt.
- Bổ sung requirement về logging, retry, tool limits, prompt regression và MCP security đã yêu cầu trong `VALIDATION.md`.
- Thêm liên kết tuần, milestone, rủi ro, DoD tháng và handoff RAG rõ ràng.
- Bổ sung tài liệu đọc cụ thể cho từng ngày, thay vì chỉ tham chiếu chung ở mức tuần/tháng.

## Open issues

- Hoàn thiện Month-02 trước khi người học thực hiện Month-03 để prerequisite không còn là giả định.
- Hoàn thiện Month-04 trước khi thực hiện handoff RAG; không tự thêm Qdrant/RAGAS vào Month-03.
- Khi source project tồn tại, đối chiếu lại chính xác tên module/route với các path dự kiến và chạy command thật.

## Recommendation for next month

Tháng 04 bắt đầu từ ingestion/chunking/metadata và giữ `LLMClient`, structured response và telemetry đã thiết lập. Thay `search_product_docs` keyword catalog bằng retrieval có citation dần dần, đồng thời xây evaluation dataset trước khi tối ưu hybrid search.
