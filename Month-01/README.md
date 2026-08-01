# Tháng 1 - Python, FastAPI, Docker và PyTorch inference cơ bản

Tháng 1 đặt nền móng cho project xuyên suốt `ai-assistant-platform`. Người học chuyển từ tư duy backend PHP/NestJS sang Python backend cho AI Engineering, nhưng không học lại REST API, Git hay Docker từ đầu. Mỗi ngày đều tạo hoặc cải thiện một phần cụ thể của project.

## Mục tiêu tháng

- Khởi tạo project Python bằng `uv`.
- Viết Python backend có type hint, dataclass, exception, logging, JSON fixture và test.
- Xây FastAPI service có router, Pydantic schema, config, dependency injection và error handling.
- Thêm async endpoint, HTTPX client có timeout, request ID middleware, Dockerfile và Docker Compose.
- Hiểu PyTorch Tensor ở mức inference: shape, dtype, device, `eval()` và `torch.no_grad()`.
- Kết thúc tháng bằng endpoint `POST /api/v1/inference/score` chạy được trong Docker.

## Kiến thức đầu vào

Người học nên có sẵn:

- Biết backend API, HTTP method, status code và JSON.
- Biết Git cơ bản: branch, commit, diff.
- Biết Docker cơ bản: image, container, port mapping.
- Đã từng làm project JavaScript/TypeScript hoặc PHP có cấu trúc module.
- Có thể đọc tài liệu tiếng Anh kỹ thuật ở mức cơ bản.

Không yêu cầu biết Python chuyên sâu, FastAPI, PyTorch, Local LLM hay OpenAI API ở tháng này.

## Kết quả đầu ra

Sau tháng 1, `ai-assistant-platform` cần có:

- Project Python quản lý bằng `uv`, có `pyproject.toml`, `uv.lock` và README riêng.
- `GET /health`, `GET /api/v1/status`, `POST /api/v1/chat` và `POST /api/v1/inference/score`.
- Request/response dùng Pydantic; domain object không bị trộn vào HTTP schema.
- Config đọc từ environment và `.env.example`, không hard-code secret.
- Logging cơ bản, request ID, timeout cho HTTP client và error response nhất quán.
- Unit test, integration test, lint bằng Ruff.
- Dockerfile và `docker-compose.yml` chạy được local.
- PyTorch toy inference service có test và demo end-to-end.

## Kiến trúc trước tháng

Trước tháng 1, project code chưa tồn tại. Repository chỉ có roadmap Markdown và yêu cầu xây dựng project chính:

```text
ai-assistant-platform/
```

## Kiến trúc sau tháng

Đến cuối tháng 1, project nên đạt cấu trúc tối thiểu sau:

```text
ai-assistant-platform/
├── app/
│   ├── api/
│   │   ├── dependencies.py
│   │   ├── routes/
│   │   │   ├── chat.py
│   │   │   ├── health.py
│   │   │   ├── inference.py
│   │   │   └── status.py
│   │   └── schemas/
│   │       ├── chat.py
│   │       └── inference.py
│   ├── core/
│   │   ├── config.py
│   │   ├── errors.py
│   │   ├── logging.py
│   │   └── middleware.py
│   ├── domain/
│   │   └── chat.py
│   ├── services/
│   │   ├── chat_service.py
│   │   ├── fixture_loader.py
│   │   ├── inference_service.py
│   │   └── status_client.py
│   └── main.py
├── docs/
│   └── month-02-handoff.md
├── scripts/
│   ├── dataloader_overview.py
│   ├── inference_mode.py
│   └── tensor_basics.py
├── tests/
│   ├── fixtures/
│   ├── integration/
│   └── unit/
├── .dockerignore
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── uv.lock
└── README.md
```

Cấu trúc này là mục tiêu học tập. Nếu người học chọn đặt project trong repository riêng, vẫn giữ tên project và module như trên để các tháng sau nối tiếp được.

## Milestone từng tuần

| Tuần | Trọng tâm | Đầu ra kiểm tra được |
| --- | --- | --- |
| [Tuần 1](./Week-01.md) | Python backend foundation và `uv` | Mock chat service có domain object, fixture JSON, logging và unit test |
| [Tuần 2](./Week-02.md) | FastAPI, Pydantic và API structure | Health endpoint, chat endpoint, config, dependency injection và error contract |
| [Tuần 3](./Week-03.md) | Async, HTTPX, Docker và integration test | Async status endpoint, timeout-aware client, request ID, Docker runtime và API integration test |
| [Tuần 4](./Week-04.md) | PyTorch Tensor và inference endpoint | Toy PyTorch scoring service, inference API và Docker smoke test |

## Nhịp học

Mỗi tuần có 7 ngày theo nhịp:

- 5 ngày học và thực hành tính năng nhỏ.
- 1 ngày milestone có test hoặc demo rõ ràng.
- 1 ngày review, refactor, tài liệu hoặc nghỉ bù.

Mỗi ngày giới hạn 60-120 phút. Nếu hết thời gian, dừng ở Definition of Done của ngày thay vì mở rộng thêm feature.

## Ghi chú command

Các lệnh trong tuần ưu tiên Bash trên macOS, Linux, WSL hoặc Git Bash. Trên Windows PowerShell:

- Thay `mkdir -p` bằng `New-Item -ItemType Directory -Force`.
- Biến môi trường một lần có thể viết `$env:APP_ENV="development"` trước khi chạy lệnh.
- Các lệnh `uv run`, `uv add`, `docker build`, `docker compose` và `curl` giữ nguyên nếu đã có trong `PATH`.

## Tài liệu tham khảo

Tài liệu chính thức được gom trong [RESOURCES.md](./RESOURCES.md). Mỗi ngày chỉ đọc phần được chỉ định trong file tuần, không cần đọc toàn bộ website.

## Definition of Done tháng

- Hoàn thành đủ 28 ngày trong [Week-01.md](./Week-01.md), [Week-02.md](./Week-02.md), [Week-03.md](./Week-03.md) và [Week-04.md](./Week-04.md).
- Tất cả ngày học đều có mục tiêu, kết quả, thời lượng, lý thuyết, tài liệu, thực hành, thay đổi project, file tạo/sửa, command, kết quả mong đợi, cách kiểm tra, Definition of Done, commit message và câu hỏi tự kiểm tra.
- `uv run pytest` và `uv run ruff check .` pass ở cuối tháng.
- Docker demo trả được health, chat mock và inference score.
- Không commit `.env`, không hard-code secret, không log raw request body.
- README của project giải thích được cách chạy local, chạy Docker và smoke test.
- `docs/month-02-handoff.md` ghi rõ Month-02 sẽ tiếp tục từ API, test, Docker và toy inference baseline hiện có.

## Rủi ro quá tải và cách giảm tải

- **Quá sa đà Python syntax:** chỉ học phần phục vụ backend module, test và API.
- **Dạy lại REST API quá sâu:** người học đã có nền backend, chỉ nhắc lại khi cần cho FastAPI contract.
- **Docker quá rộng:** chỉ cần Dockerfile và Compose cho API, không thêm PostgreSQL, Redis, Qdrant.
- **PyTorch thành training course:** tháng này chỉ inference; training loop để Month-02.
- **Async bị dùng sai:** chỉ dùng async cho I/O hoặc route minh họa; không coi async là cách làm CPU-bound inference nhanh hơn.

## Nội dung được phép bỏ qua nếu thiếu thời gian

- Tối ưu Docker image nâng cao.
- Custom logging formatter phức tạp.
- Test quá chi tiết cho log message.
- GPU setup.
- DataLoader script nếu đã hiểu rõ batch concept và cần giữ ngày 26 dưới 90 phút.

Không được bỏ qua: `uv`, FastAPI, Pydantic schema, config, logging cơ bản, test, Docker demo và PyTorch inference endpoint.

## Cầu nối sang Month-02

Month-02 sẽ dùng nền Month-01 để học data processing, ML foundation, Neural Network và Transformer foundation. Điểm nối bắt buộc là `docs/month-02-handoff.md`: endpoint inference hiện chỉ là toy model, nhưng đã có API boundary, service layer, test và Docker runtime để gắn data pipeline và training script sau này.
