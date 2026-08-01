# Tháng 6 — Tuần 4: Observability, quality regression và bàn giao portfolio

## Mục tiêu tuần

Hoàn thiện vòng vận hành cho `ai-assistant-platform`: metrics, JSON log, LangSmith trace đã redact, ngân sách token/cost, quality regression RAG/agent định kỳ, runbook, kiến trúc và demo có thể tái hiện. Đây là tuần đo và bàn giao, không bắt đầu local model serving hay dashboard cluster.

## Kiến thức cần đạt

- Logs giải thích sự kiện đơn lẻ, metrics theo dõi xu hướng/alert, trace nối một request qua agent/RAG/tool.
- Latency, error rate, token/cost và quality là các signal bổ sung; không kết luận sức khỏe bằng một metric.
- Scheduled evaluation cần golden set, baseline, threshold, report và error analysis để có giá trị regression.

## Tính năng project sẽ bổ sung

`app/observability/metrics.py`, `app/observability/usage.py`, `scripts/run_quality_regression.py`, `.github/workflows/quality-regression.yml`, `docs/observability.md`, `docs/runbook.md`, `docs/architecture.md`, `docs/demo-script.md`, `README.md` của project và ADR cuối tháng.

## Kế hoạch từng ngày

### Ngày 22 — Signal catalogue và metric contract

- **Mục tiêu:** Chọn ít signal vận hành nhưng trả lời được câu hỏi khi API/agent/RAG suy giảm.
- **Kết quả cần đạt:** Có catalogue metric với name, type, label allowlist, unit, owner và action cho request count/error, latency, readiness, tool budget/approval outcome.
- **Phân bổ thời gian:** 20 phút review JSON logs, 25 phút đọc metrics, 45 phút thiết kế/implement counter-histogram adapter, 15 phút test = 105 phút.
- **Lý thuyết:** Counter, histogram, gauge; high-cardinality label như `request_id`, user query hay thread ID không phù hợp metric label.
- **Tài liệu:** [OpenTelemetry metrics concepts](https://opentelemetry.io/docs/concepts/signals/metrics/) — metric types và attributes.
- **Bài thực hành:** Ghi metric contract trước, thêm adapter có interface fake/no-op; đo route/status/latency không lưu prompt.
- **Tích hợp project:** Instrument FastAPI boundary và graph outcome, giữ request ID ở log/trace thay vì metric label.
- **File tạo/sửa:** `app/observability/metrics.py`, `docs/observability.md`, `tests/unit/test_metrics_contract.py`.
- **Lệnh chạy:** `uv run pytest tests/unit/test_metrics_contract.py -q`.
- **Kết quả mong đợi:** Test từ chối label không allowlist; snapshot metric không có query, email, token hay secret.
- **Cách kiểm tra:** `rg -n "request_id|query|thread_id" app/observability/metrics.py` chỉ cho phép ở comment/guard, không ở labels.
- **Definition of Done:** Mỗi metric có mục đích và owner/action, không thu thập "mọi thứ".
- **Commit message gợi ý:** `feat(observability): add bounded service metric contract`
- **Câu hỏi tự kiểm tra:** Vì sao request ID không là metric label? Histogram dùng để trả lời gì? Metric nào chỉ ra readiness outage?

### Ngày 23 — Token usage, cost budget và latency breakdown

- **Mục tiêu:** Ghi nhận usage/cost ước lượng theo request an toàn để nhận biết ngân sách bị vượt.
- **Kết quả cần đạt:** Usage event có model alias, input/output token, latency stage và cost estimate từ pricing config version; event thiếu usage không làm request fail.
- **Phân bổ thời gian:** 15 phút xem LLM client, 25 phút đọc usage, 50 phút implement/test, 15 phút báo cáo mẫu = 105 phút.
- **Lý thuyết:** Token usage từ provider khác cost estimate; price table/version cần được review, không hard-code token giá trị bí mật.
- **Tài liệu:** [OpenAI Responses API reference](https://platform.openai.com/docs/api-reference/responses) — trường usage và theo dõi usage (đọc khái niệm; không đưa API key vào test).
- **Bài thực hành:** Map response usage đã mock thành event, phân đoạn `retrieval_ms`, `llm_ms`, `total_ms`; đặt soft budget cảnh báo và hard policy ở service nếu project đã có quyền áp dụng.
- **Tích hợp project:** Correlate event bằng request ID đã hash/trace ID metadata, không log raw conversation hay authorization header.
- **File tạo/sửa:** `app/observability/usage.py`, `app/core/cost_policy.py`, `tests/unit/test_usage_accounting.py`, `docs/observability.md`.
- **Lệnh chạy:** `uv run pytest tests/unit/test_usage_accounting.py -q`.
- **Kết quả mong đợi:** Fixture có usage tạo cost estimate xác định; fixture thiếu usage tạo `unknown` có reason, không bịa số.
- **Cách kiểm tra:** Review event JSON; chi phí có currency/version và không có API key/prompt.
- **Definition of Done:** Budget alert có owner/action; cost estimate được ghi là estimate, không là invoice.
- **Commit message gợi ý:** `feat(observability): account for token usage and estimated cost`
- **Câu hỏi tự kiểm tra:** Token count có luôn bằng bill không? Vì sao pricing version cần lưu? Nếu provider không trả usage thì làm gì?

### Ngày 24 — LangSmith tracing sampling và privacy review

- **Mục tiêu:** Nối HTTP request, LangGraph nodes và LLM/tool spans bằng trace opt-in có redaction/sampling.
- **Kết quả cần đạt:** Trace adapter mặc định no-op khi thiếu cấu hình; production config sample rate rõ, redact prompt/authorization/secret và propagates request correlation metadata tối thiểu.
- **Phân bổ thời gian:** 20 phút rà trace Month-05, 25 phút đọc docs, 45 phút adapter/test, 15 phút privacy review = 105 phút.
- **Lý thuyết:** Trace giúp causal debugging; sampling giảm chi phí/dữ liệu nhưng không thay audit log approval.
- **Tài liệu:** [LangSmith tracing with OpenTelemetry](https://docs.langchain.com/langsmith/trace-with-opentelemetry) — tracing setup và export.
- **Bài thực hành:** Thêm `TRACE_ENABLED`/`TRACE_SAMPLE_RATE` validation, fake exporter test và redaction recursive cho headers/config.
- **Tích hợp project:** Retain `request_id`, route, safe graph outcome và approval id; vẫn không gửi raw RAG documents/user prompt nếu policy chưa consent.
- **File tạo/sửa:** `app/observability/tracing.py`, `tests/unit/test_trace_redaction.py`, `docs/observability.md`.
- **Lệnh chạy:** `uv run pytest tests/unit/test_trace_redaction.py -q`.
- **Kết quả mong đợi:** Trace disabled không gọi network; enabled fixture không chứa `sk-`, `Bearer` hoặc raw prompt.
- **Cách kiểm tra:** `rg -n "Authorization|Bearer|sk-" artifacts tests` sau fixture không có output nhạy cảm.
- **Definition of Done:** Sampling/redaction policy nêu data owner, retention review và cách tắt trace khẩn cấp.
- **Commit message gợi ý:** `feat(tracing): add opt-in redacted agent traces`
- **Câu hỏi tự kiểm tra:** Sampling làm mất thông tin nào? Trace thay audit log không? Vì sao trace disabled vẫn cần test?

### Ngày 25 — Scheduled RAG/agent quality regression

- **Mục tiêu:** Chạy golden datasets thành quality gate định kỳ mà không gọi production data hoặc một LLM judge duy nhất.
- **Kết quả cần đạt:** Runner xuất JSON/Markdown report có dataset version, baseline/current, metrics retrieval+groundedness+route/tool policy, threshold và failure cases.
- **Phân bổ thời gian:** 15 phút kiểm tra datasets, 25 phút đọc evaluation, 50 phút runner/workflow, 15 phút test report = 105 phút.
- **Lý thuyết:** Unit/integration test kiểm contract; evaluation đo chất lượng xác suất. Threshold cần baseline và human review lane.
- **Tài liệu:** [Ragas evaluation concepts](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/) — lựa chọn metric; dùng DeepEval runner Month-05 nếu đó là tool đã chọn.
- **Bài thực hành:** Combine fixture RAG golden set và agent scenario set; scheduled workflow chỉ upload report safe, fail khi deterministic policy hoặc threshold đã phê duyệt bị vi phạm.
- **Tích hợp project:** Reuse `evals/rag/` và `evals/agent/`; không tạo dataset mới từ log người dùng hay bỏ citation/approval cases.
- **File tạo/sửa:** `scripts/run_quality_regression.py`, `.github/workflows/quality-regression.yml`, `evals/reports/README.md`.
- **Lệnh chạy:** `uv run python scripts/run_quality_regression.py --mode fixture --write-report artifacts/quality-report.json`.
- **Kết quả mong đợi:** Report phân biệt skipped/not-run/failed; có baseline so sánh trước/sau và không có một score tổng che lỗi safety.
- **Cách kiểm tra:** Thay fixture citation sai, runner phải nêu case ID/metric lỗi và exit code theo policy.
- **Definition of Done:** Workflow chạy theo schedule và manual dispatch; secret-required judge được optional/explicit, fixture path vẫn lặp lại offline.
- **Commit message gợi ý:** `ci(quality): schedule RAG and agent regression reports`
- **Câu hỏi tự kiểm tra:** Vì sao score trung bình có thể che safety regression? Baseline nằm ở đâu? Khi nào evaluation chỉ nên warn thay vì block?

### Ngày 26 — Alert specification và error analysis

- **Mục tiêu:** Chuyển signal thành phản ứng vận hành, không chỉ tạo dashboard đẹp.
- **Kết quả cần đạt:** Có alert spec cho sustained error/latency, readiness, cost anomaly và quality regression; error taxonomy liên kết case ID, owner, severity và action.
- **Phân bổ thời gian:** 20 phút đọc reports, 25 phút chọn thresholds, 40 phút viết spec, 15 phút tabletop alert = 100 phút.
- **Lý thuyết:** Alert cần symptom, window, severity, runbook link và tránh alert fatigue; SLO/threshold phải là giả định có thể điều chỉnh.
- **Tài liệu:** [Google SRE workbook: alerting](https://sre.google/workbook/alerting-on-slos/) — alert dựa trên user impact và response.
- **Bài thực hành:** Viết 4 alert cards (condition, window, owner, first diagnostic, mitigation); phân loại failure retrieval/citation/route/tool/approval/provider.
- **Tích hợp project:** Alert link tới request log, trace redacted, quality report và deployment rollback runbook; không thêm Prometheus/Grafana bắt buộc.
- **File tạo/sửa:** `docs/alert-spec.md`, `docs/error-taxonomy.md`, `docs/runbook.md`.
- **Lệnh chạy:** `uv run python scripts/run_quality_regression.py --mode fixture --write-report artifacts/quality-report.json`.
- **Kết quả mong đợi:** Mỗi alert có một action giới hạn/đảo ngược được; không có alert theo từng request ID.
- **Cách kiểm tra:** Tabletop: provider timeout 10 phút và citation regression; dùng spec để chọn người/command/rollback, ghi câu trả lời.
- **Definition of Done:** Threshold không được tuyên bố universal; source, owner và review cadence được ghi rõ.
- **Commit message gợi ý:** `docs(operations): add alerts and quality failure taxonomy`
- **Câu hỏi tự kiểm tra:** Alert nào cần page ngay? Vì sao high-cardinality metric nguy hiểm? Error analysis khác counter lỗi thế nào?

### Ngày 27 — Architecture, ADR, runbook và demo script

- **Mục tiêu:** Viết tài liệu đủ cho reviewer/maintainer hiểu system, quyết định và cách demo an toàn.
- **Kết quả cần đạt:** Architecture nêu boundary FastAPI/Nginx/agent/RAG/persistence/observability; ADR giải thích single-EC2 Compose; demo có happy path, refusal và approval path.
- **Phân bổ thời gian:** 15 phút inventory, 40 phút viết diagram/docs, 30 phút dry-run demo, 20 phút link review = 105 phút.
- **Lý thuyết:** ADR ghi context/decision/consequences, không là nhật ký; runbook là action under pressure.
- **Tài liệu:** [Architecture Decision Records](https://adr.github.io/) — format ADR; xem lại docs deploy/CI/evaluation trong project.
- **Bài thực hành:** Cập nhật `README.md` project với prerequisites, local start, test/eval, security note và demo evidence; script demo tránh input nhạy cảm, destructive tool và secret.
- **Tích hợp project:** Liên kết trực tiếp đến Month-04 citation evaluation, Month-05 HITL, Month-06 deploy/rollback; không tuyên bố hệ thống autonomous.
- **File tạo/sửa:** `docs/architecture.md`, `docs/adr/007-single-ec2-production-scope.md`, `docs/runbook.md`, `docs/demo-script.md`, `README.md`.
- **Lệnh chạy:** `uv run pytest; docker compose -f docker-compose.prod.yml config`.
- **Kết quả mong đợi:** Người mới biết cách chạy demo/mock, xem known limitations và không cần secret để đọc tài liệu.
- **Cách kiểm tra:** Link-check nội bộ, đi theo demo script trên fixture và xác nhận approval export không tự thực thi.
- **Definition of Done:** Architecture có data flow + trust boundary; runbook có rollback/incident/evaluation commands với expected result.
- **Commit message gợi ý:** `docs(portfolio): add architecture runbook and safe demo script`
- **Câu hỏi tự kiểm tra:** ADR khác README thế nào? Demo nào chứng minh HITL? Boundary nào bảo vệ secret?

### Ngày 28 — Final milestone: portfolio demo, review và handoff

- **Mục tiêu:** Xác minh toàn chuỗi Month-06 và chuẩn bị portfolio handoff trung thực.
- **Kết quả cần đạt:** Có final demo evidence, review checklist, known limitations/backlog và báo cáo status PASS/PASS_WITH_NOTES theo điều kiện AWS/domain thật.
- **Phân bổ thời gian:** 15 phút preflight, 40 phút demo+quality run, 25 phút test/lint/config, 20 phút review/portfolio = 100 phút.
- **Lý thuyết:** Production readiness là tập hợp bằng chứng có hạn và phải nói rõ phần chưa được thực thi vì external gate.
- **Tài liệu:** Xem lại [README Month-06](./README.md), `docs/runbook.md`, `docs/release-checklist.md` và [VALIDATION.md](../VALIDATION.md).
- **Bài thực hành:** Chạy local production-like demo: health/ready, RAG citation/refusal, agent approval, quality runner và CI smoke; record revision, report path, blockers.
- **Tích hợp project:** Hoàn thiện README portfolio với feature, architecture, run command, test/evaluation evidence, observability và security limitations.
- **File tạo/sửa:** `docs/final-demo-evidence.md`, `README.md`, `docs/month-06-final-handoff.md`.
- **Lệnh chạy:** `uv run ruff check .; uv run mypy app; uv run pytest; uv run python scripts/run_quality_regression.py --mode fixture; docker build -t ai-assistant-platform:final .`.
- **Kết quả mong đợi:** Các command có output/evidence; TLS/EC2 được ghi PASS chỉ nếu thực chạy, nếu không là NOT_RUN với prerequisite cụ thể.
- **Cách kiểm tra:** Đối chiếu checklist dưới với `VALIDATION.md`, mở toàn bộ internal links của Month 06 và kiểm tra không có secret/placeholder.
- **Definition of Done:** Bàn giao có thể tái tạo local và không che giấu limitation cloud/domain hoặc quality failures.
- **Commit message gợi ý:** `docs(month-06): finalize production portfolio handoff`
- **Câu hỏi tự kiểm tra:** Bằng chứng nào chứng minh quality gate? Điều gì không thể khẳng định nếu chưa có domain? Người vận hành mới bắt đầu incident ở đâu?

## Milestone cuối tuần

Project có catalogue signal, token/cost estimate, trace privacy policy, scheduled quality regression, alert spec, architecture/runbook/demo/portfolio README và final handoff có evidence.

## Review checklist

- [ ] Logs, metrics và traces không chứa prompt/secret/raw authorization header.
- [ ] Cost/latency/error/quality có metric, owner và action riêng.
- [ ] Regression dùng datasets/baseline/threshold/failure analysis, không chỉ LLM judge.
- [ ] Runbook, ADR, architecture và demo links hoạt động; cloud result ghi trung thực.

## Definition of Done

Hoàn thành bảy ngày và có một portfolio handoff vận hành được tại local production-like scope, với CI/release/observability/evaluation documents nối liền Month-04 và Month-05.

## Lỗi thường gặp

- Gọi tracing là monitoring nhưng không redact hoặc không có sampling.
- Alert mỗi lỗi lẻ gây noise, không link hành động.
- Chạy evaluation không baseline/threshold/error analysis.
- Bổ sung Ollama/vLLM, Kubernetes hoặc dashboard cluster để né việc hoàn thiện runbook.

## Tài liệu tham khảo chính thức

Xem [RESOURCES.md](./RESOURCES.md), nhóm Tuần 4.

## Nội dung tùy chọn nếu còn thời gian

Chỉ đọc overview Ollama/vLLM để hiểu local serving trade-off, không cài đặt/benchmark; hoặc thêm dashboard HTML tĩnh từ report đã redact.
