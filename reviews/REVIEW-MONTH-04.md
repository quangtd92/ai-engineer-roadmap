# Month 04 Review

## Status

PASS_WITH_NOTES

## Scope

Triển khai curriculum riêng cho Month-04: README, Week-01 đến Week-04 và kiểm tra liên kết/nội dung liên quan. Không chỉnh sửa Month-05 hoặc Month-06.

## Files reviewed

- `Month-04/README.md`
- `Month-04/RESOURCES.md`
- `Month-04/Week-01.md`
- `Month-04/Week-02.md`
- `Month-04/Week-03.md`
- `Month-04/Week-04.md`
- `ROADMAP_SPEC.md`, `VALIDATION.md`, `IMPLEMENTATION_PLAN.md`
- Handoff Month-03 và Week-01 Month-05 (chỉ đọc để kiểm tra liên tục)

## Deliverables verified

- [x] README nêu mục tiêu, prerequisite, đầu ra, kiến trúc trước/sau, bốn milestone, rủi ro/giảm tải, Definition of Done và handoff.
- [x] Bốn tuần có đúng 28 ngày: 01–07, 08–14, 15–21 và 22–28.
- [x] Mỗi ngày có mục tiêu, output, thời lượng, lý thuyết, tài liệu, thực hành, project integration, files, command, expected result, verification, DoD, commit message và câu hỏi tự kiểm tra.
- [x] Progression triển khai ingestion/chunking → Qdrant/dense/BM25/hybrid → rewrite/rerank/citation/safety → dataset/evaluation/report.
- [x] Có dense baseline và hybrid+rerank comparison; có evaluation dataset, threshold, error analysis, RAGAS **hoặc** DeepEval và regression gate.

## Validation summary

### Repository structure

PASS_WITH_NOTES — Sáu file thuộc Month-04 và report review tồn tại, không rỗng. README liên kết đến bốn tuần, resources và review bằng path tương đối hợp lệ. Repository cấp toàn cục vẫn có những tháng chưa hoàn thiện theo `VALIDATION.md`; nằm ngoài phạm vi task này.

### Daily completeness

PASS — Có 28 heading ngày, mỗi ngày là một thay đổi riêng có đầu ra kiểm tra được. Ngày milestone/review tổng hợp phần đã học, không thêm framework lớn mới.

### Time budget

PASS — Mọi ngày ghi 90–120 phút; không ngày nào vượt 120 phút. RAGAS/DeepEval là một lựa chọn duy nhất cho evaluator bắt buộc và credential được đánh dấu optional, nên không biến secret/quota thành yêu cầu học.

### Technical sequence

PASS — Month-03 cung cấp LLM adapter/Structured Output; Week-01 tạo data contract trước storage; Week-02 tạo retrieval trước reranking/answer; Week-03 xác thực citation/refusal/injection trước evaluation; Week-04 chỉ đo và bàn giao read-only RAG sang LangGraph Month-05. Không dạy agent, human approval hay deployment sớm.

### Project progression

PASS — Tất cả bài tập thay đổi `ai-assistant-platform`: corpus allowlist, ingestion, Qdrant, BM25/hybrid, answer API, test/eval và demo. Capability được bàn giao có input/output, timeout, citation và refusal boundary để Month-05 tái sử dụng thay vì sao chép RAG.

### References and internal links

PASS — Link nội bộ Markdown trong phạm vi Month-04/review được kiểm tra; nguồn kỹ thuật dùng Python, Qdrant, OpenAI, Pydantic, RAGAS, DeepEval và pytest. Mỗi ngày trỏ tới phần đọc cụ thể hoặc nguồn chính thức tương ứng, không dùng URL tự tạo.

### Security

PASS — Ingestion chỉ nhận path tương đối trong allowlist; parser giới hạn extension; corpus không chứa secret/PII; Qdrant URL/config không hard-code credential; logs tránh raw document/secret; request có timeout/fallback. Week-03 xử lý prompt injection trong retrieved document, citation validation và refusal khi evidence thiếu. Không có thao tác destructive lên collection trong command.

### Evaluation

PASS — Golden JSONL có provenance/no-answer cases; deterministic retrieval metrics (hit@k, MRR), latency và comparison được tách khỏi LLM-as-judge. Report yêu cầu baseline, threshold, per-case failure taxonomy và action. Regression gate chạy offline; RAGAS/DeepEval chỉ bổ sung grounded-answer signal.

## Technical checks performed

- [x] Đếm heading ngày: Week-01=7, Week-02=7, Week-03=7, Week-04=7.
- [x] Kiểm tra mỗi ngày có 14 trường bắt buộc theo curriculum contract.
- [x] Kiểm tra toàn bộ time budget nằm trong 60–120 phút; mức thực tế của Month-04 là 90–120 phút.
- [x] Kiểm tra relative links từ Month-04 và report không tham chiếu file thiếu.
- [x] Tìm template/placeholder trong bốn Week files; Week-03 và Week-04 không còn template tiếng Anh.
- [x] So sánh `git diff` để bảo đảm Month-05 và Month-06 không bị sửa.

## Issues found

1. Lúc bắt đầu task, Week-03 và Week-04 là template ngắn, không có lịch 7 ngày hay trường bắt buộc.
2. Repository không chứa source code/project runnable hiện tại; command, path và test là kế hoạch triển khai có thể kiểm tra khi `ai-assistant-platform` được tạo theo tháng trước.
3. RAGAS/DeepEval có thể cần credential/model tùy evaluator; không thể xem kết quả online là điều kiện pass cho curriculum.

## Issues fixed

- Thay template Week-03 bằng tuần query rewrite, reranking, bounded context, verified citation, evidence refusal và document prompt-injection defense.
- Thay template Week-04 bằng dataset, dense baseline, hybrid comparison, offline regression gate, evaluator option, error analysis, demo và handoff.
- Hoàn thiện README với review link và boundary rõ ràng sang Month-05.
- Sửa lịch từ dự thảo 30 ngày về chính xác 28 ngày.

## Open issues

- Khi project code tồn tại, xác nhận lại đường dẫn module/route dự kiến và chạy thật `uv run pytest`, `uv run ruff check .`, Docker/Qdrant và evaluator theo dependency lock.
- Xác minh bằng browser khi xuất bản công khai nếu một external documentation URL đổi đường dẫn; internal links đã được kiểm tra trong workspace.
- Cần hoàn thiện các tháng ngoài phạm vi theo checklist repository-level trước khi tuyên bố toàn bộ roadmap hoàn chỉnh.

## Recommendation for next month

Month-05 chỉ nên dùng `rag_answer`/`rag_search` như capability read-only, có timeout, status, citations và refusal đã được đánh giá. Graph không được tự ingest, upsert/delete collection hoặc bypass citation/evidence policy; human approval áp dụng cho hành động nhạy cảm của agent, không thay thế các boundary này.
