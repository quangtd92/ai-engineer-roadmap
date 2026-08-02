# Tháng 6 — Tuần 1: Production hardening

## Mục tiêu tuần

Tạo một image FastAPI production-like cho agent/RAG hiện có: cấu hình an toàn, probes tách biệt, log truy vết được, giới hạn request và kiểm tra dependency.

## Kiến thức cần đạt

- Phân biệt liveness `/health` với readiness `/ready`; readiness kiểm tra dependency cần cho traffic.
- Dùng multi-stage Dockerfile, `.dockerignore`, immutable image tag và non-root runtime.
- Giới hạn secret/log, request size, rate và header tại ranh giới HTTP.

## Feature hoặc module sẽ bổ sung

`src/ai_assistant_platform/api/routes/health.py`, `src/ai_assistant_platform/core/settings.py`, `src/ai_assistant_platform/observability/logging.py`, middleware production, `Dockerfile`, `.dockerignore`, `docker-compose.prod.yml`, `tests/integration/test_probes.py` và `scripts/check_dependencies.py`.

## Kế hoạch từng ngày

### Ngày 1 — Production configuration và secret boundary

**Mục tiêu:** Tách cấu hình development/production mà không để secret lọt vào code hoặc log.

**Kết quả cần đạt:** `Settings` fail-fast khi thiếu biến bắt buộc ở production và `.env.example` chỉ chứa tên biến.

**Phân bổ thời gian:** 15 phút rà config Month-05; 25 phút đọc; 45 phút sửa settings; 15 phút test = 100 phút.

**Lý thuyết cần học:** Twelve-factor config; secret là dữ liệu runtime, không phải build argument hay source.

**Tài liệu cần đọc:** [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) — dotenv, validation và env prefix.

**Bài thực hành:** Thêm `APP_ENV`, `OPENAI_API_KEY`, `DATABASE_URL`, `LANGSMITH_API_KEY`; dùng giá trị giả trong test và redact field nhạy cảm khi render config.

**Tích hợp project:** `create_app()` chỉ bật debug/docs theo `APP_ENV`; startup trả lỗi rõ khi production thiếu key.

**File tạo hoặc sửa:** `src/ai_assistant_platform/core/settings.py`, `.env.example`, `.gitignore`, `tests/unit/test_settings.py`.

**Lệnh cần chạy:** `uv run pytest tests/unit/test_settings.py -q`

**Kết quả mong đợi:** Test chứng minh secret không xuất hiện trong `repr`/log và missing production config bị chặn.

**Cách tự kiểm tra:** `rg -n "(sk-|API_KEY=.+)" .env.example app` không được thấy key thật; không add `.env` vào Git.

**Definition of Done:** Có test cho valid/missing/redacted settings và `.env.example` không có giá trị bí mật.

**Commit message gợi ý:** `feat(config): validate production settings and redact secrets`

**Câu hỏi tự kiểm tra:** Vì sao build arg không phù hợp secret? Biến nào cần fail-fast? Log config có thể rò gì?

### Ngày 2 — Health và readiness probes

**Mục tiêu:** Thiết kế endpoint để orchestrator phân biệt process sống với dịch vụ sẵn sàng nhận traffic.

**Kết quả cần đạt:** `/health` không gọi network; `/ready` kiểm tra connection nhẹ tới dependency bắt buộc với timeout ngắn.

**Phân bổ thời gian:** 10 phút ôn config; 25 phút đọc; 50 phút code/test probes; 15 phút curl = 100 phút.

**Lý thuyết cần học:** Liveness lỗi không nên restart vì outage downstream; readiness có thể trả 503 để load balancer ngừng gửi traffic.

**Tài liệu cần đọc:** [FastAPI status codes](https://fastapi.tiangolo.com/tutorial/response-status-code/) — trả 200/503 rõ nghĩa.

**Bài thực hành:** Tạo dependency `ReadinessChecker`, fake Redis/PostgreSQL trong test, đặt timeout 1 giây và payload không chứa connection string.

**Tích hợp project:** Đăng ký router probes trước router chat/agent để Docker/Nginx có đường kiểm tra ổn định.

**File tạo hoặc sửa:** `src/ai_assistant_platform/api/routes/health.py`, `src/ai_assistant_platform/services/readiness.py`, `tests/integration/test_probes.py`.

**Lệnh cần chạy:** `uv run pytest tests/integration/test_probes.py -q`

**Kết quả mong đợi:** `/health` là 200 khi dependency fake down; `/ready` là 503 với `{"status":"not_ready"}`.

**Cách tự kiểm tra:** Chạy app local rồi `curl -i http://localhost:8000/health` và mock dependency down trong test.

**Definition of Done:** Hai endpoint có contract/test riêng và không log exception chain chứa secret.

**Commit message gợi ý:** `feat(health): add liveness and readiness probes`

**Câu hỏi tự kiểm tra:** Probe nào dùng cho restart? Vì sao readiness cần timeout? 503 khác 500 thế nào?

### Ngày 3 — Structured logging và correlation ID

**Mục tiêu:** Làm mọi request production có log JSON truy vết được mà không lưu nội dung nhạy cảm.

**Kết quả cần đạt:** Log request có `request_id`, route, status, latency_ms và error class; response trả `X-Request-ID`.

**Phân bổ thời gian:** 10 phút xem middleware cũ; 25 phút đọc; 50 phút implement; 15 phút xem log = 100 phút.

**Lý thuyết cần học:** Structured event, correlation ID và cardinality; không log prompt, token, authorization header hay secret.

**Tài liệu cần đọc:** [Python logging cookbook](https://docs.python.org/3/howto/logging-cookbook.html) — contextual information.

**Bài thực hành:** Dùng `contextvars`/logging filter, lấy header hợp lệ hoặc sinh UUID; viết test asserting field thay vì nguyên câu log.

**Tích hợp project:** Truyền request ID vào service agent và LangSmith metadata để nối HTTP log với trace.

**File tạo hoặc sửa:** `src/ai_assistant_platform/observability/logging.py`, `src/ai_assistant_platform/api/middleware/request_context.py`, `tests/unit/test_request_logging.py`.

**Lệnh cần chạy:** `uv run pytest tests/unit/test_request_logging.py -q`

**Kết quả mong đợi:** Một request tạo JSON line và header cùng request ID, không có `Authorization`/prompt raw.

**Cách tự kiểm tra:** Gửi request lỗi có header Authorization giả, tìm log bằng `rg "Authorization|Bearer"` không có kết quả.

**Definition of Done:** Event schema và redaction test được commit; latency dùng monotonic clock.

**Commit message gợi ý:** `feat(observability): add structured request logging`

**Câu hỏi tự kiểm tra:** Correlation ID giúp debug xuyên service ra sao? Field nào có cardinality cao? Vì sao không log prompt mặc định?

### Ngày 4 — Multi-stage Docker image và non-root runtime

**Mục tiêu:** Biến image local thành artifact tối thiểu, tái lập và ít quyền hơn.

**Kết quả cần đạt:** Dockerfile có builder/runtime stage, cài dependency từ `uv.lock`, chạy UID không phải root và không copy `.env`.

**Phân bổ thời gian:** 15 phút kiểm tra Dockerfile hiện có; 25 phút đọc; 50 phút build/run; 20 phút inspect = 110 phút.

**Lý thuyết cần học:** Layer cache, lockfile, attack surface, `COPY --from` và signal handling của process chính.

**Tài liệu cần đọc:** [Docker multi-stage builds](https://docs.docker.com/build/building/multi-stage/) — named stages và final runtime.

**Bài thực hành:** Đặt `USER app`, thêm `.dockerignore`, tag `ai-assistant-platform:local`, pin base image digest nếu team có policy.

**Tích hợp project:** Image chạy `uvicorn ai_assistant_platform.main:app`; expose 8000 và dùng `/health` làm container healthcheck ở Compose ngày 5.

**File tạo hoặc sửa:** `Dockerfile`, `.dockerignore`, `docs/container.md`.

**Lệnh cần chạy:** `docker build -t ai-assistant-platform:local .`

**Kết quả mong đợi:** Build thành công; `docker run --rm -p 8000:8000 ai-assistant-platform:local` không cần source mount.

**Cách tự kiểm tra:** `docker image inspect ai-assistant-platform:local` và `docker run --rm --entrypoint id ai-assistant-platform:local` hiển thị UID non-root.

**Definition of Done:** Không có `.env`, `.git`, `.venv` trong build context; runtime không chạy root.

**Commit message gợi ý:** `build(docker): harden production image with multi-stage build`

**Câu hỏi tự kiểm tra:** Builder và runtime stage khác gì? Lockfile đảm bảo điều gì? Non-root còn cần file permission nào?

### Ngày 5 — Compose production-like và container healthcheck

**Mục tiêu:** Ghi rõ cấu hình runtime không dùng cho development và kiểm tra dependency startup đúng thứ tự.

**Kết quả cần đạt:** `docker-compose.prod.yml` dùng image tag, env file local ignored, restart policy, named volumes và healthcheck.

**Phân bổ thời gian:** 10 phút ôn image; 25 phút đọc; 50 phút compose; 15 phút inspect = 100 phút.

**Lý thuyết cần học:** `depends_on` health condition không thay readiness; volume state phải được backup độc lập.

**Tài liệu cần đọc:** [Compose startup order](https://docs.docker.com/compose/how-tos/startup-order/) — healthcheck và `depends_on`.

**Bài thực hành:** Tách override local khỏi production; expose API chỉ trên loopback chuẩn bị cho Nginx; thêm resource limit như một ghi chú theo Docker runtime.

**Tích hợp project:** Định nghĩa services API/Redis/PostgreSQL/Qdrant theo đúng dependency đã dùng ở Month-04/05, không thêm service mới vì "cho đủ".

**File tạo hoặc sửa:** `docker-compose.prod.yml`, `deploy/.env.prod.example`, `docs/container.md`.

**Lệnh cần chạy:** `docker compose -f docker-compose.prod.yml config`

**Kết quả mong đợi:** Compose render hợp lệ; `docker compose ... up -d` chỉ báo API healthy sau readiness pass.

**Cách tự kiểm tra:** `docker compose -f docker-compose.prod.yml ps` và `docker inspect` xem health status.

**Definition of Done:** Production compose không bind-mount source, không chứa secret thật và dùng named volume có tên rõ.

**Commit message gợi ý:** `build(compose): add production runtime configuration`

**Câu hỏi tự kiểm tra:** Vì sao source mount không phù hợp production? Healthcheck Docker khác readiness API ra sao? Volume nào có state?

### Ngày 6 — Rate limit, security headers và request boundary

**Mục tiêu:** Thêm giới hạn rẻ ở API trước khi LLM/tool tốn chi phí.

**Kết quả cần đạt:** Có middleware/route policy cho request size, rate limit theo client và headers an toàn; 429 có request ID.

**Phân bổ thời gian:** 15 phút threat review; 25 phút đọc; 45 phút implement; 15 phút test = 100 phút.

**Lý thuyết cần học:** Rate limit bảo vệ availability/cost, không thay authentication; proxy header chỉ tin khi Nginx được cấu hình trusted.

**Tài liệu cần đọc:** [OWASP secure headers project](https://owasp.org/www-project-secure-headers/) — mục tiêu của các response header.

**Bài thực hành:** Giới hạn body theo `Content-Length`/stream policy, dùng in-memory limiter cho local và interface thay Redis backend; thêm `X-Content-Type-Options`, `Referrer-Policy`, `Cache-Control: no-store` cho chat.

**Tích hợp project:** Bỏ qua rate limit cho `/health`; không bypass approval, tool budget hay guardrail Month-05.

**File tạo hoặc sửa:** `src/ai_assistant_platform/api/middleware/security.py`, `src/ai_assistant_platform/core/rate_limit.py`, `tests/integration/test_security_boundary.py`.

**Lệnh cần chạy:** `uv run pytest tests/integration/test_security_boundary.py -q`

**Kết quả mong đợi:** Request thứ N vượt quota trả 429, body quá lớn trả 413 và headers xuất hiện trên API response.

**Cách tự kiểm tra:** Test không phụ thuộc clock thật; kiểm tra response 429 không lộ quota key hoặc user data.

**Definition of Done:** Có test cho allowed/blocked paths và cấu hình limit được đọc từ Settings.

**Commit message gợi ý:** `feat(api): add rate limits and security headers`

**Câu hỏi tự kiểm tra:** 429 nên có gì? Vì sao health endpoint không cùng limiter? Rate limit có ngăn prompt injection không?

### Ngày 7 — Milestone hardening và dependency scan

**Mục tiêu:** Kết hợp hardening tuần 1 thành một smoke test và ghi các rủi ro chưa xử lý.

**Kết quả cần đạt:** Production image build/run, probes/log/boundary test pass và dependency audit có report được review.

**Phân bổ thời gian:** 15 phút checklist; 20 phút đọc audit; 55 phút chạy milestone; 20 phút ghi issue = 110 phút.

**Lý thuyết cần học:** Vulnerability scan tạo tín hiệu cần triage theo exploitability; không tự động nâng package major trong ngày milestone.

**Tài liệu cần đọc:** [pip-audit documentation](https://pypi.org/project/pip-audit/) — audit environment/requirements và exit code.

**Bài thực hành:** Thêm script audit phù hợp lockfile; chạy Ruff, mypy, pytest, build image và curl probes; ghi CVE/false positive vào `docs/security-review.md`.

**Tích hợp project:** Đây là release-candidate image sẽ được chuyển sang EC2 ở Week-02, không deploy nếu smoke test fail.

**File tạo hoặc sửa:** `scripts/check_dependencies.py`, `docs/security-review.md`, `docs/release-checklist.md`.

**Lệnh cần chạy:** `uv run ruff check .; uv run mypy app; uv run pytest; docker build -t ai-assistant-platform:rc .`

**Kết quả mong đợi:** Các gate pass hoặc có issue được phân loại/blocker rõ ràng; không công bố image có high-risk chưa quyết định.

**Cách tự kiểm tra:** Lưu output audit làm artifact local, kiểm tra `docker compose ... ps` và hai probe HTTP.

**Definition of Done:** Có checklist signed-off local, security findings không bị bỏ qua im lặng và Week-02 prerequisite rõ.

**Commit message gợi ý:** `chore(release): add hardening smoke checks`

**Câu hỏi tự kiểm tra:** Scan khác triage thế nào? Lỗi nào chặn deploy? Vì sao không update dependency mù quáng?

## Milestone cuối tuần

Tag `ai-assistant-platform:rc` build được, chạy Compose production-like, liveness/readiness có test, log JSON có correlation ID, runtime non-root và API có boundary tối thiểu.

## Review checklist

- [ ] `.env`/secret không nằm trong image, source hay log.
- [ ] `/health` và `/ready` có semantics/test khác nhau.
- [ ] Container chạy non-root, image dùng lockfile và `.dockerignore`.
- [ ] 429/413/security headers có integration test.
- [ ] Audit được triage, không chỉ chạy cho có.

## Definition of Done

Hoàn thành 7 ngày, tất cả lệnh kiểm tra pass hoặc issue ghi rõ; có image RC sẵn sàng cho deployment rehearsal.

## Những lỗi thường gặp

- Dùng `/health` để kiểm tra database khiến app bị restart khi dependency outage.
- Copy `.env` vào image hoặc in cả Settings khi debug.
- Tin `X-Forwarded-For` trước khi đặt trusted proxy.
- Cho rate limiter in-memory làm giải pháp multi-instance production.

## Tài liệu tham khảo chính thức

- [Docker multi-stage builds](https://docs.docker.com/build/building/multi-stage/) — builder/runtime stage.
- [Dockerfile reference: HEALTHCHECK](https://docs.docker.com/reference/dockerfile/#healthcheck) — semantics và options.
- [FastAPI deployment concepts](https://fastapi.tiangolo.com/deployment/concepts/) — process và HTTPS proxy.
- [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) — configuration từ environment.

## Nội dung tùy chọn nếu còn thời gian

Đo image size trước/sau multi-stage, hoặc thay in-memory limiter bằng adapter Redis đã có; không thêm reverse proxy trước Week-02.
