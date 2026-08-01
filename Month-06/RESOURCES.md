# Tháng 6 — Tài liệu tham khảo

Mỗi ngày chỉ đọc đúng phần được dẫn từ tuần. Link dưới đây đã được mở kiểm tra khi biên soạn; ưu tiên tài liệu chính thức và không yêu cầu tạo tài khoản/secret để đọc.

## Tuần 1 — Production hardening

- [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) — dotenv, environment và validation.
- [Docker multi-stage builds](https://docs.docker.com/build/building/multi-stage/) — builder/runtime stages.
- [Dockerfile HEALTHCHECK](https://docs.docker.com/reference/dockerfile/#healthcheck) — healthcheck semantics.
- [FastAPI deployment concepts](https://fastapi.tiangolo.com/deployment/concepts/) — process và HTTPS proxy.

## Tuần 2 — EC2 và reverse proxy

- [AWS EC2 getting started](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EC2_GetStarted.html) — instance, key pair, security group và storage.
- [Docker Engine security](https://docs.docker.com/engine/security/) — daemon và quyền Docker.
- [Nginx Beginner’s Guide](https://nginx.org/en/docs/beginners_guide.html) — server block, proxy và reload.
- [Certbot User Guide](https://eff-certbot.readthedocs.io/en/stable/using.html) — obtain, renew và dry-run.
- [Docker volumes](https://docs.docker.com/engine/storage/volumes/) — lifecycle/backup volume.

## Tuần 3 — CI/CD

- [GitHub: Building and testing Python](https://docs.github.com/en/actions/tutorials/build-and-test-code/python) — workflow Python, test và artifact.
- [uv: GitHub Actions integration](https://docs.astral.sh/uv/guides/integration/github/) — setup/cache và lockfile.
- [GitHub: managing deployment environments](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments) — approval/protection/environment secret.
- [Docker: GitHub Actions build](https://docs.docker.com/build/ci/github-actions/) — build/push/caching.
- [GitHub Actions workflow syntax](https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions) — events, permissions và concurrency.

## Tuần 4 — Observability và quality

- [OpenTelemetry metrics](https://opentelemetry.io/docs/concepts/signals/metrics/) — signals, metric type và attributes.
- [OpenAI Responses API reference](https://platform.openai.com/docs/api-reference/responses) — trường `usage` trong response; chỉ dùng mock trong test nếu không có key.
- [LangSmith tracing with OpenTelemetry](https://docs.langchain.com/langsmith/trace-with-opentelemetry) — opt-in tracing và export.
- [Ragas available metrics](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/) — metric selection cho RAG evaluation.
- [Google SRE: Alerting on SLOs](https://sre.google/workbook/alerting-on-slos/) — user-impact alerts và response.

## Tìm hiểu thêm

Ollama/vLLM chỉ là overview sau khi hoàn thành toàn bộ required work. Không thêm Kubernetes, TensorRT, SGLang hoặc framework observability thứ hai vào lộ trình bắt buộc.
