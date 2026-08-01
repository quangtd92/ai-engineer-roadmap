# Final Repository Review

## Status

PASS_WITH_NOTES

## Scope

Technical-curriculum review toàn bộ roadmap 6 tháng theo `ROADMAP_SPEC.md`, `VALIDATION.md` và `AGENTS.md`. Review kiểm tra curriculum và tính hợp lệ cấu trúc/link; không xác nhận AWS, domain, API key hay source code runtime vì repository hiện chỉ chứa roadmap.

## Files reviewed

- `README.md`, `00-Prerequisites.md`, `ROADMAP_SPEC.md`, `VALIDATION.md`.
- Sáu `Month-XX/README.md`, 24 `Week-XX.md`, sáu `RESOURCES.md` và sáu `REVIEW.md`.
- Sáu báo cáo canonical `REVIEW-MONTH-01.md` đến `REVIEW-MONTH-06.md`.

## Validation summary

| Hạng mục | Status | Bằng chứng / nhận định |
| --- | --- | --- |
| 6 tháng, 24 tuần | PASS | Có `Month-01`…`Month-06`, mỗi tháng có đúng bốn file tuần. |
| Ngày học | PASS | 24 file tuần có bảy kế hoạch ngày, tổng 168 ngày. Số ngày tăng tuần tự trong từng tháng; cách viết `01`/`1` chỉ là format, không tạo trùng lặp. |
| Ngân sách 1–2 giờ | PASS | Daily plans phân bổ 60–120 phút; milestone không yêu cầu quá 120 phút. Cloud/domain/API real được đặt thành optional hoặc manual gate. |
| Không lặp máy móc | PASS | Trọng tâm tiến triển từ foundation → LLM/tool → RAG → agent → production; ngày review/buffer có mục đích kiểm tra/handoff riêng. |
| Thứ tự dependency | PASS | FastAPI/test/async xuất hiện trước LLM; Structured Output và bounded Tool Calling xuất hiện trước MCP/RAG; RAG có citation/evaluation trước khi trở thành capability của LangGraph. |
| Project progression | PASS_WITH_NOTES | Mỗi tuần chỉ định module/endpoint/test cụ thể cho `ai-assistant-platform`. Đây là repository curriculum, chưa có source project để chạy xác minh. |
| Công nghệ trước khi giới thiệu | PASS | Qdrant/RAGAS ở Month-04, LangGraph/HITL ở Month-05, EC2/Nginx/CI production ở Month-06. |
| Evaluation sớm | PASS | Month-03 có schema/tool-result/prompt regression; Month-04 có golden set, baseline, RAGAS/DeepEval và error analysis; Month-05 có agent eval; Month-06 có scheduled quality regression. |
| Tool Calling vs Agent | PASS | Month-03 dạy tool read-only, deterministic registry, bounded closed loop. Month-05 dạy `StateGraph`, conditional routing, checkpoint, interrupt/resume, approval và side-effect policy. |
| Month-02 ML scope | PASS | Linear Regression chỉ là foundation; Logistic Regression là baseline chính. Không bắt buộc SVM, KNN, PCA, XGBoost tuning hay tự train Transformer. |
| Month-06 production scope | PASS | Một EC2 + Docker Compose, Nginx, CI, logs/metrics/traces/runbook; HTTPS/DNS/AWS là manual gate. Không bắt buộc Kubernetes, local-serving benchmark hay cluster monitoring. |
| README navigation | PASS | README chính nay liên kết đến toàn bộ 6 tháng và 24 tuần. |
| Internal links | PASS | Quét 187 Markdown destinations; không có destination file bị thiếu. |
| External references | PASS_WITH_NOTES | Quét 122 URL HTTPS độc nhất; sửa một DeepEval RAG URL 404 và một OpenAI Usage URL 404. Một số host trả 403/429 hoặc lỗi CA ở môi trường checker; chúng được giữ vì là nguồn official và không có bằng chứng HTTP 4xx thực tế ngoài rate-limit/access policy. |

## Issues found and fixed

1. `Month-03` thiếu `RESOURCES.md`.
   - Đã thêm tài liệu chính thức cho Responses API, Structured Output, Evals, Function Calling và MCP.
2. Sáu thư mục tháng thiếu `REVIEW.md`, dù bản review canonical tồn tại ở root.
   - Đã thêm `Month-XX/REVIEW.md` làm điểm điều hướng có status/scope, không nhân bản toàn bộ báo cáo.
3. README chính chỉ liệt kê progression, không có links đến tháng/tuần.
   - Đã thay bằng điều hướng đầy đủ cho 6 tháng và 24 tuần.
4. DeepEval RAG URL cũ trả 404.
   - Đã đổi thành `https://deepeval.com/docs/getting-started-rag`.
5. OpenAI Usage guide cũ trả 404.
   - Đã thay bằng Responses API reference, là nguồn trực tiếp cho trường `usage` mà bài học cần đọc.
6. Bốn README tháng liên kết thẳng tới review root.
   - Đã liên kết qua `./REVIEW.md` để navigation trong tháng nhất quán.

## Open issues

- Không có source `ai-assistant-platform`, lockfile hay CI workflow thực trong repository này; vì vậy chỉ xác minh được curriculum contract, không chạy `uv`, Docker, AWS hay test project.
- URL official có thể bị chặn bởi rate limit, bot protection hoặc certificate store của máy kiểm tra. Khi xuất bản ở môi trường khác, chạy lại link checker có retry/rate limit trước khi tuyên bố mọi URL đều HTTP 200.
- Các ngày API thật, EC2, DNS và HTTPS vẫn cần credential/quota/domain của người học; roadmap đã ghi rõ là optional/manual gate và không được đánh dấu đã deploy khi chưa thực hiện.

## Recommendation

Curriculum có thể dùng làm lộ trình 6 tháng. Khi bắt đầu triển khai, tạo `ai-assistant-platform` theo Month-01 và sau mỗi tháng cập nhật báo cáo canonical bằng kết quả lệnh/test thực tế, đặc biệt ở các manual gate cloud và evaluation baseline.
