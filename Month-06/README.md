# Tháng 6 — Production, Cloud, CI/CD và Observability

## Mục tiêu tháng

Đưa `ai-assistant-platform` từ workflow agent đã kiểm soát ở Month-05 thành một dịch vụ có thể demo an toàn: image production, cấu hình bí mật, reverse proxy HTTPS, pipeline CI/CD, telemetry, quality regression và tài liệu vận hành. Phạm vi là một EC2 đơn với Docker Compose; không học Kubernetes hay tự vận hành local LLM.

## Kiến thức đầu vào

- FastAPI, Pydantic, `uv`, Docker Compose, test và logging từ Month-01.
- LLM, structured output, tool/MCP và prompt regression từ Month-03.
- RAG có citation, RAGAS/DeepEval dataset và báo cáo từ Month-04.
- LangGraph có checkpoint, retry/timeout, tool budget, human approval, guardrail và LangSmith tracing từ Month-05.

Nếu Month-02 đến Month-05 chưa được triển khai chi tiết trong repository, dùng các deliverable trên như **hợp đồng đầu vào**; không bỏ qua chúng khi làm bài tập Month-06.

## Kết quả đầu ra

- Production image chạy bằng non-root user, có `/health` và `/ready`, structured log, rate limit và security headers.
- Triển khai Docker Compose trên AWS EC2 sau Nginx; HTTPS được cấp sau khi domain DNS đã trỏ đúng.
- GitHub Actions kiểm tra format/lint/type/test, build image và deploy có approval môi trường.
- Dashboard/alert specification cho latency, error rate, token/cost; LangSmith tracing và regression RAG/agent chạy định kỳ.
- `docs/runbook.md`, `docs/architecture.md`, ADR, demo script và portfolio README có thể dùng để bàn giao.

## Kiến trúc trước tháng

```text
Client -> FastAPI -> LangGraph agent -> LLM/tools/RAG
                         |                |
                    checkpoint         LangSmith trace
```

Ứng dụng chạy local bằng Docker Compose, có tests/evaluation nhưng chưa có release gate, reverse proxy, deployment runbook hay telemetry vận hành hoàn chỉnh.

## Kiến trúc sau tháng

```text
Internet -> Nginx (TLS, headers, rate limit) -> FastAPI container
                                                |-> LangGraph/RAG/LLM
GitHub Actions -> test + image -> approved deploy on EC2
FastAPI -> JSON logs + metrics + LangSmith -> alert/review + quality reports
PostgreSQL/Redis/Qdrant volumes -> backup procedure
```

## Milestone từng tuần

| Tuần | Milestone kiểm tra được |
|---|---|
| [01](./Week-01.md) | `docker compose` chạy production-like với probes, non-root image, request log và protection cơ bản. |
| [02](./Week-02.md) | EC2 chạy stack sau Nginx; HTTPS và rollback được ghi thành runbook (chỉ thực hiện TLS khi có domain). |
| [03](./Week-03.md) | Pull request CI chạy lint/type/test/build; deploy workflow có environment approval và release checklist. |
| [04](./Week-04.md) | Metrics/traces/regression report, runbook, ADR, demo và portfolio README hoàn chỉnh. |

## Nhịp học và nguyên tắc an toàn

Mỗi ngày 70–120 phút, một trọng tâm chính. Không commit `.env`, private key, token LangSmith, GitHub secret hay URL webhook. Secret chỉ tồn tại trong `.env` local (ignored), GitHub Environment/EC2 secret store; log chỉ ghi tên cấu hình và request ID, không ghi giá trị secret, prompt nhạy cảm hoặc authorization header.

Các lệnh `ssh`, DNS, Certbot và deploy là **manual gate**: chỉ chạy sau khi người học có EC2/domain/quyền hợp lệ. Không tạo AWS resource hoặc public endpoint trong giáo trình này.

## Definition of Done tháng

- [ ] Hoàn thành 28 ngày, mỗi ngày 70–120 phút và có bằng chứng chạy/test.
- [ ] Image production không chứa `.env`, chạy non-root và health/readiness phân biệt đúng.
- [ ] Nginx, EC2 deployment, persistent volumes, backup và rollback được thử hoặc ghi rõ prerequisite chưa có.
- [ ] CI có lint, type check, unit/integration test, build; deploy cần protected environment.
- [ ] Có metric, trace, budget token/cost, regression RAG/agent và error analysis định kỳ.
- [ ] Có runbook, architecture, ADR, demo script, portfolio README và review tháng.

## Rủi ro quá tải và cách giảm tải

| Rủi ro | Cách giảm tải |
|---|---|
| Vừa học AWS, Nginx, TLS và deploy | Chỉ dùng một EC2 + Compose; tách provisioning, proxy, TLS, rollback thành ngày riêng. |
| Chưa có domain/AWS account | Hoàn thành config, runbook và local smoke test; đánh dấu TLS/deploy là manual prerequisite, không bịa kết quả. |
| CI chậm hoặc flaky | Chạy unit/test trước, integration trong job riêng; cache `uv`, lưu artifact report. |
| Monitoring biến thành dự án lớn | Bắt đầu bằng metrics/structured logs/LangSmith và alert specification; không thêm Prometheus cluster bắt buộc. |

## Nội dung được phép bỏ qua nếu thiếu thời gian

- MLflow, Ollama và vLLM chỉ đọc overview vào Ngày 26; không cài hay benchmark local serving.
- CDK/IaC, blue-green deploy, autoscaling, WAF và dashboard Grafana là phần mở rộng.
- Nếu không có domain, mô phỏng Nginx local và hoàn thành hướng dẫn TLS/renewal thay vì cố tạo certificate không hợp lệ.

## Cầu nối từ Month-05 và sang portfolio

Tuần 1 đóng gói agent đã có approval/guardrail; tuần 2 đưa đúng image đó lên EC2; tuần 3 biến các kiểm tra đã học thành release gate; tuần 4 đo chất lượng và tạo tài liệu để người khác vận hành, đánh giá và demo sản phẩm.

## Điều hướng

- [Tuần 1 — Production hardening](./Week-01.md)
- [Tuần 2 — EC2, Nginx, HTTPS và rollback](./Week-02.md)
- [Tuần 3 — CI/CD và release discipline](./Week-03.md)
- [Tuần 4 — Observability, quality và handoff](./Week-04.md)
- [Báo cáo tự review](./REVIEW.md)
- [Tài liệu tham khảo đã xác minh](./RESOURCES.md)
