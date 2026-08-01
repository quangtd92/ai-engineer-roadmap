# Tháng 6 — Tuần 3: GitHub Actions, CI/CD và kỷ luật release

## Mục tiêu tuần

Biến các kiểm tra đã có thành release gate trên GitHub Actions: lint, type check, unit/integration test, evaluation offline và build image. Deploy chỉ có workflow chuẩn bị artifact/SSH command sau protected environment; không cấp AWS credential hay tự deploy từ nhánh chưa được review.

## Kiến thức cần đạt

- CI chứng minh artifact từ commit hiện tại qua checks; CD chỉ được chạy khi environment policy phê duyệt.
- Test không thay evaluation: RAG/agent regression tạo report, có threshold và failure artifact riêng.
- Secret GitHub chỉ dùng runtime, masked không đồng nghĩa an toàn để in log.

## Tính năng project sẽ bổ sung

`.github/workflows/ci.yml`, `.github/workflows/deploy.yml`, `.github/dependabot.yml`, `scripts/ci_smoke.ps1`, `docs/ci-cd.md`, `docs/release-checklist.md` và `docs/month-06-week-03-handoff.md`.

## Kế hoạch từng ngày

### Ngày 15 — Thiết kế pipeline và branch protection contract

- **Mục tiêu:** Vẽ pipeline từ pull request đến production để tách checks bắt buộc, artifact và approval.
- **Kết quả cần đạt:** `docs/ci-cd.md` có flow PR → CI → image digest → protected `production` → deploy/manual rollback và bảng secret theo tên/owner.
- **Phân bổ thời gian:** 20 phút rà commands cũ, 25 phút đọc GitHub Docs, 45 phút viết diagram, 15 phút review = 105 phút.
- **Lý thuyết:** Event `pull_request` khác `push`/`workflow_dispatch`; branch protection không phải test runner.
- **Tài liệu:** [Building and testing Python](https://docs.github.com/en/actions/tutorials/build-and-test-code/python) — workflow, Python setup và artifacts.
- **Bài thực hành:** Chọn một Python version từ `pyproject.toml`, phân nhóm unit/integration/evaluation, ghi permission tối thiểu `contents: read` cho CI.
- **Tích hợp project:** Các gate dùng đúng `uv run ruff check .`, `uv run mypy app`, `uv run pytest`, và runner eval Month-04/05 đã bàn giao.
- **File tạo/sửa:** `docs/ci-cd.md`, `docs/release-checklist.md`.
- **Lệnh chạy:** `uv run ruff check .; uv run mypy app; uv run pytest`.
- **Kết quả mong đợi:** Không job nào cần OpenAI key để unit test; quality job có chế độ fixture/offline.
- **Cách kiểm tra:** Map từng command vào một job và chỉ ra artifact/failure action; review không có credential value.
- **Definition of Done:** Pipeline design ghi rõ gate nào block merge và gate nào block deploy.
- **Commit message gợi ý:** `docs(ci): define release gates and environment ownership`
- **Câu hỏi tự kiểm tra:** Vì sao deploy không chạy ở every PR? Unit test khác evaluation artifact ra sao? Permission tối thiểu nào đủ?

### Ngày 16 — CI lint, type check và unit test với uv

- **Mục tiêu:** Tạo workflow nhanh cho feedback PR, cài dependency từ lockfile thay vì dùng pip làm package manager chính.
- **Kết quả cần đạt:** `ci.yml` checkout, setup Python/uv, sync locked dependency, Ruff, mypy và unit tests; failure log chỉ chứa command/error an toàn.
- **Phân bổ thời gian:** 15 phút xem workflow syntax, 25 phút đọc caching, 50 phút viết/test YAML, 15 phút local parity = 105 phút.
- **Lý thuyết:** Lockfile tạo dependency reproducibility; cache chỉ tối ưu thời gian, không là nguồn chân lý.
- **Tài liệu:** [uv GitHub Actions integration](https://docs.astral.sh/uv/guides/integration/github/) — setup, cache và `uv sync --locked`.
- **Bài thực hành:** Trigger `pull_request`/`push` phù hợp, cache theo `uv.lock`, chạy `uv run pytest tests/unit` tách khỏi integration.
- **Tích hợp project:** Reuse test settings/fake clients để LLM, LangSmith và database thật không được yêu cầu trong PR job.
- **File tạo/sửa:** `.github/workflows/ci.yml`, `scripts/ci_smoke.ps1`.
- **Lệnh chạy:** `pwsh -File scripts/ci_smoke.ps1 -Stage unit`.
- **Kết quả mong đợi:** Local smoke command và YAML dùng cùng commands; linter/type fail trả exit code khác 0.
- **Cách kiểm tra:** Cố ý tạo fixture type/lint lỗi trên branch thử (không commit) và xác nhận script dừng đúng stage.
- **Definition of Done:** Workflow pin action version theo policy dự án, không cache `.env` hoặc upload log có secret.
- **Commit message gợi ý:** `ci: add locked uv lint type and unit test workflow`
- **Câu hỏi tự kiểm tra:** Cache miss có làm sai kết quả không? Vì sao CI dùng `--locked`? Test fake client bảo vệ điều gì?

### Ngày 17 — Integration test và artifact báo cáo

- **Mục tiêu:** Chạy integration test có dependency rõ ràng và lưu report hữu ích khi thất bại.
- **Kết quả cần đạt:** Job integration khởi động dịch vụ tối thiểu hoặc Compose profile test, timeout, upload JUnit/coverage/evaluation report khi job kết thúc.
- **Phân bổ thời gian:** 20 phút inventory tests, 25 phút đọc artifacts, 45 phút implement job, 15 phút kiểm tra paths = 105 phút.
- **Lý thuyết:** Service container/Compose test cần health wait; artifact là evidence, không thay log redaction.
- **Tài liệu:** [GitHub Actions storing workflow data as artifacts](https://docs.github.com/en/actions/how-tos/writing-workflows/choosing-what-your-workflow-does/storing-and-sharing-data-from-a-workflow) — upload/download artifact.
- **Bài thực hành:** Chạy probes, proxy contract và agent/RAG fixtures; dùng `if: always()` cho report không nhạy cảm và retention ngắn theo policy.
- **Tích hợp project:** Test contract `/health`/`/ready`, approval boundary và citation regression, không gọi OpenAI hay deploy EC2 trong CI.
- **File tạo/sửa:** `.github/workflows/ci.yml`, `pytest.ini`, `docs/ci-cd.md`.
- **Lệnh chạy:** `uv run pytest tests/integration -q --junitxml=artifacts/junit.xml`.
- **Kết quả mong đợi:** Job fail nếu service không ready; artifact có report chứ không có database dump/prompt raw.
- **Cách kiểm tra:** Inspect artifact allowlist và tắt một fake dependency để xác nhận timeout message hữu ích.
- **Definition of Done:** Integration path ghi rõ prerequisite và có thể chạy local bằng command tương đương.
- **Commit message gợi ý:** `ci: add integration checks and safe test artifacts`
- **Câu hỏi tự kiểm tra:** `if: always()` dùng cho việc gì? Vì sao không upload `.env` để debug? Integration test khác deployment rehearsal nào?

### Ngày 18 — Build image, SBOM/audit và image promotion

- **Mục tiêu:** Đưa image build vào CI như artifact có định danh, chỉ promote khi checks pass.
- **Kết quả cần đạt:** Job build tạo tag theo commit SHA, kiểm tra Dockerfile, chạy dependency audit đã triage và xuất SBOM/audit report nếu tool đang có trong project.
- **Phân bổ thời gian:** 15 phút đọc Docker action, 25 phút threat review, 50 phút workflow build, 15 phút test local = 105 phút.
- **Lý thuyết:** Image tag dễ đọc không thay digest; scan finding cần triage chứ không cập nhật dependency mù quáng.
- **Tài liệu:** [Docker build GitHub Actions](https://docs.docker.com/build/ci/github-actions/) — build/push pattern và cache.
- **Bài thực hành:** Build `ai-assistant-platform:${GITHUB_SHA}`, không push registry nếu chưa có registry credential; lưu metadata/digest và script audit output đã redact.
- **Tích hợp project:** Build chính Dockerfile multi-stage non-root Tuần 1, không tạo Dockerfile CI khác.
- **File tạo/sửa:** `.github/workflows/ci.yml`, `docs/security-review.md`, `docs/ci-cd.md`.
- **Lệnh chạy:** `docker build -t ai-assistant-platform:ci .; uv run python scripts/check_dependencies.py`.
- **Kết quả mong đợi:** Build fail làm CI fail; finding high-risk chưa triage block release theo checklist.
- **Cách kiểm tra:** `docker image inspect ai-assistant-platform:ci` và xác nhận report không chứa lockfile secrets/credential.
- **Definition of Done:** Image source revision và audit decision được liên kết trong release evidence.
- **Commit message gợi ý:** `ci: build revision-tagged production image with audit evidence`
- **Câu hỏi tự kiểm tra:** Digest dùng để làm gì? Scan fail nào phải block? Vì sao build không đồng nghĩa deploy?

### Ngày 19 — Deploy workflow với protected environment

- **Mục tiêu:** Viết deploy workflow an toàn, bắt đầu bằng preview/dry-run và chờ phê duyệt môi trường.
- **Kết quả cần đạt:** `deploy.yml` chỉ chạy `workflow_dispatch`/tag hợp lệ, tham chiếu environment `production`, validate image tag và gọi script deploy idempotent sau approval.
- **Phân bổ thời gian:** 20 phút đọc environment controls, 40 phút viết YAML/script, 30 phút dry-run, 15 phút review = 105 phút.
- **Lý thuyết:** Environment protection rule giới hạn ai/khi nào truy cập environment secret; approval workflow không thay human approval cho agent action.
- **Tài liệu:** [Managing environments for deployment](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments) — protection rules và environment secrets.
- **Bài thực hành:** Ghi `DEPLOY_HOST`, `DEPLOY_USER`, `DEPLOY_SSH_KEY` là *tên* secret; script chỉ nhận revision, kiểm tra `/ready` rồi dừng/rollback theo runbook.
- **Tích hợp project:** Reuse `scripts/rollback.ps1` và `docs/runbook.md`; deploy không chạy migration phá huỷ hay reset Qdrant.
- **File tạo/sửa:** `.github/workflows/deploy.yml`, `scripts/deploy.ps1`, `docs/ci-cd.md`.
- **Lệnh chạy:** `pwsh -File scripts/deploy.ps1 -Revision dry-run -WhatIf`.
- **Kết quả mong đợi:** Dry-run không tạo network connection hoặc thay đổi host; workflow thiếu environment approval không thể xem production secret.
- **Cách kiểm tra:** Review trigger and permissions line-by-line; xác nhận image revision là input bắt buộc, không dùng `latest`.
- **Definition of Done:** Có manual rollback path và deploy condition không dựa vào PR title/branch name mơ hồ.
- **Commit message gợi ý:** `ci: add protected environment deployment workflow`
- **Câu hỏi tự kiểm tra:** Vì sao `latest` nguy hiểm khi rollback? Environment secret xuất hiện ở job nào? CI approval có phê duyệt export report không?

### Ngày 20 — Release checklist, version và rollback decision

- **Mục tiêu:** Biến tiêu chí kỹ thuật thành quyết định release có bằng chứng và owner.
- **Kết quả cần đạt:** Checklist yêu cầu CI green, scan triage, quality threshold, backup state, approver, image digest và post-deploy probes; có bảng go/no-go.
- **Phân bổ thời gian:** 20 phút review gates, 30 phút hoàn thiện checklist, 35 phút tabletop incident, 15 phút update ADR = 100 phút.
- **Lý thuyết:** Semantic version/tag là giao tiếp; rollback criteria cần định trước outage, không quyết bằng cảm giác.
- **Tài liệu:** [GitHub release management](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository) — tag và release notes.
- **Bài thực hành:** Mô phỏng release quality threshold fail và readiness fail; chọn no-go/rollback, ghi evidence đã xem chứ không chạy deploy thật.
- **Tích hợp project:** Checklist gọi report RAG/agent Month-04/05 và backup rehearsal Tuần 2, không chỉ nhìn pytest pass.
- **File tạo/sửa:** `docs/release-checklist.md`, `docs/adr/006-release-and-rollback.md`.
- **Lệnh chạy:** `uv run pytest; uv run python evals/rag/run_rag_eval.py --mode fixture`.
- **Kết quả mong đợi:** Có một decision log mẫu fail hợp lệ; release không được proceed khi threshold/report thiếu.
- **Cách kiểm tra:** Đưa checklist cho người khác: họ xác định được ai approve, artifact nào dùng và khi nào rollback.
- **Definition of Done:** Không có mục "deploy nếu ổn" mơ hồ; tất cả tiêu chí có command, evidence hoặc manual owner.
- **Commit message gợi ý:** `docs(release): add evidence-based go no-go checklist`
- **Câu hỏi tự kiểm tra:** Test xanh có đủ release không? Ai phê duyệt môi trường? Điều gì khác rollback image và rollback data?

### Ngày 21 — Milestone: mô phỏng pull request tới release

- **Mục tiêu:** Chạy toàn bộ pipeline local/CI, review workflow như code và ghi handoff observability.
- **Kết quả cần đạt:** PR simulation có lint/type/unit/integration/build/eval evidence; deploy ở dry-run/approved environment đúng trạng thái thực tế.
- **Phân bổ thời gian:** 15 phút preflight, 50 phút chạy gates, 20 phút review YAML, 15 phút handoff = 100 phút.
- **Lý thuyết:** CI/CD reliability bao gồm recovery from failed workflow và artifact traceability.
- **Tài liệu:** Xem lại [Workflow syntax](https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions) — events, permissions và concurrency.
- **Bài thực hành:** Chạy `ci_smoke`, validate YAML, giả lập job fail bằng test fixture; ghi cách rerun an toàn mà không reusing secret in log.
- **Tích hợp project:** Tạo handoff Week 4 với location logs/metrics/traces/reports và image revision convention.
- **File tạo/sửa:** `docs/month-06-week-03-handoff.md`, `docs/ci-cd.md`.
- **Lệnh chạy:** `pwsh -File scripts/ci_smoke.ps1 -Stage all; docker build -t ai-assistant-platform:rc .`.
- **Kết quả mong đợi:** Các gate có evidence hoặc blocker cụ thể; không đánh dấu deploy PASS khi chỉ mới dry-run.
- **Cách kiểm tra:** Review checklist dưới đây và kiểm tra links tới runbook/release checklist không hỏng.
- **Definition of Done:** Một PR reviewer có thể tái tạo checks và hiểu điều kiện deploy/rollback trong 10 phút.
- **Commit message gợi ý:** `docs(ci): record release pipeline rehearsal and observability handoff`
- **Câu hỏi tự kiểm tra:** Concurrency bảo vệ điều gì? Artifact nào hỗ trợ postmortem? Khi workflow fail, bước đầu tiên là gì?

## Milestone cuối tuần

Pull request có CI lặp lại được; image revision có evidence; deploy workflow cần protected environment và có dry-run/rollback path. Không cần registry/AWS account để hoàn thành phần kiểm tra cục bộ.

## Review checklist

- [ ] CI dùng `uv`/lockfile, tách unit và integration, không cần key thật.
- [ ] Report artifact đã allowlist và redact; quality gate không bị bỏ qua.
- [ ] Build tag theo revision, finding security được triage.
- [ ] Deploy chỉ bằng approved environment và revision xác định; không `latest`.

## Definition of Done

Hoàn thành bảy ngày với pipeline kiểm chứng code lẫn artifact release; deployment vẫn giữ manual/environment boundary và không thay sự phê duyệt hành động nhạy cảm của agent.

## Lỗi thường gặp

- Nhét secret vào YAML, artifact hoặc echo debug.
- Chạy integration gọi API LLM thật làm CI flaky/tốn chi phí.
- Push/deploy từ mọi branch và dùng tag `latest`.
- Bỏ qua quality regression vì unit tests đã pass.

## Tài liệu tham khảo chính thức

Xem [RESOURCES.md](./RESOURCES.md), nhóm Tuần 3.

## Nội dung tùy chọn nếu còn thời gian

Thêm Dependabot cho dependency updates hoặc cache build có đo thời gian. Không thêm ArgoCD, Jenkins hay pipeline thứ hai.
