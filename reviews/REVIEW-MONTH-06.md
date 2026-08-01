# Month 06 Review

## Status

PASS_WITH_NOTES

## Scope

Rà soát nội dung curriculum Month-06: README, bốn tuần, resource list, liên kết nội bộ và tính liên tục từ Month-05. Đây là review tài liệu; không tuyên bố rằng người học đã thực hiện deploy AWS/domain thật.

## Files reviewed

- `Month-06/README.md`
- `Month-06/RESOURCES.md`
- `Month-06/Week-01.md` đến `Month-06/Week-04.md`
- `Month-05/README.md`, `Month-05/Week-04.md`, `Month-05/RESOURCES.md`
- `ROADMAP_SPEC.md`, `VALIDATION.md`, `IMPLEMENTATION_PLAN.md`

## Deliverables verified

- 28 ngày, bốn tuần; mỗi tuần có objective, kiến thức/module, milestone, checklist, DoD, lỗi thường gặp, nguồn và nội dung tùy chọn.
- Mỗi ngày có mục tiêu, kết quả, thời lượng 100–110 phút, lý thuyết, tài liệu, thực hành, tích hợp `ai-assistant-platform`, file, command, expected result, verification, DoD, commit và câu hỏi tự kiểm tra.
- Chuỗi kỹ thuật: hardening/image → EC2/Nginx/TLS/rollback → CI/CD protected deploy → metrics/tracing/cost/quality/portfolio.
- Handoff Month-05 được tái sử dụng: agent approval/guardrail, checkpoint/RAG dependencies, LangSmith redaction và datasets evaluation.
- Resources ưu tiên official documentation; AWS/domain/Certbot/deploy đều được gắn manual gate, không cần secret hoặc tạo cloud resource.

## Validation summary

### Repository structure

PASS — Month-06 có README, Week-01..04 và `RESOURCES.md`; report ở cấp repository là `REVIEW-MONTH-06.md` theo convention các tháng hiện có. README liên kết bốn tuần, resources và review.

### Daily completeness

PASS — 28/28 ngày dùng nội dung riêng; không còn placeholder “Learn one focused topic” ở Week-02..04. Week-01 vốn đã chi tiết và được giữ nguyên.

### Time budget

PASS — Tất cả ngày Month-06 nêu 100–110 phút (nằm trong 70–120 phút) và giữ một trọng tâm chính. Không có ngày bắt buộc quá hai giờ.

### Technical sequence

PASS — Không đưa Kubernetes/local serving nâng cao vào required work. Nginx/TLS xuất hiện sau production image/probes; CI deploy xuất hiện sau deployment rehearsal; scheduled evaluation xuất hiện sau RAG/agent dataset và CI foundation.

### Project progression

PASS — Mỗi tuần bổ sung artifact kiểm chứng được vào cùng project: Docker/security, deployment/runbook, workflows/release, observability/evaluation/portfolio. Không tạo project độc lập.

### References and internal links

PASS_WITH_NOTES — Đã kiểm tra các target nội bộ `Week-01`..`Week-04`, `RESOURCES.md` và review tồn tại. Nguồn mới là tài liệu chính thức/uy tín, đã được mở kiểm tra khi biên soạn. Một số command là contract cho project sẽ được người học tạo, nên không thể chạy trong repository roadmap Markdown hiện tại.

### Security

PASS — Secret handling, redaction, non-root image, rate limit, proxy boundary, restricted SSH, TLS key handling, protected environment, backup/rollback và trace privacy đều có bài tập/verification. Các thao tác cloud, SSH, Certbot là manual gate.

### Evaluation

PASS — Tuần 4 tái sử dụng golden sets Month-04/05, có baseline/current, retrieval/groundedness/route/tool-policy, threshold, report, scheduled/manual runner và error taxonomy; không kết luận từ một metric duy nhất.

## Issues found

1. Week-02, Week-03 và Week-04 ban đầu chỉ là template tiếng Anh, thiếu gần như toàn bộ tiêu chí cấp ngày.
2. Month-06 chưa có `RESOURCES.md`, mặc dù README/tuần cần dẫn nguồn chính thức nhất quán.
3. README chưa liên kết resources.
4. EC2/HTTPS có phụ thuộc tài khoản, quyền SSH và domain; không thể chứng minh deployment thật chỉ bằng curriculum.

## Issues fixed

1. Thay ba tuần template bằng 21 ngày chi tiết, độc lập về trọng tâm và phát triển cùng `ai-assistant-platform`.
2. Thêm `Month-06/RESOURCES.md` với nhóm nguồn theo tuần.
3. Bổ sung link resources vào README Month-06.
4. Gắn manual gates, trạng thái `NOT_RUN` trung thực và rehearsal local cho các bước cần external access.

## Open issues

- Repository hiện là roadmap, không chứa source `ai-assistant-platform`; vì vậy commands/file paths trong curriculum là kế hoạch thực hành, chưa thể execution-test tại đây.
- AWS EC2, DNS và HTTPS chỉ có thể được đánh dấu PASS sau khi người học có account/domain/quyền tương ứng và lưu evidence không nhạy cảm.
- `VALIDATION.md` mô tả `REVIEW.md` trong từng tháng, còn repository hiện dùng `REVIEW-MONTH-XX.md` ở root cho các tháng 01–05. Giữ convention hiện hữu để tránh thay đổi phạm vi rộng.

## Recommendation for next month

Đây là tháng cuối. Sau khi learner làm project thật, chạy lại checklist này với evidence CI, image digest, demo fixture, report evaluation và trạng thái EC2/TLS thực tế; chỉ khi đó mới nâng status cloud/TLS từ `NOT_RUN` lên `PASS`.
