# Kế hoạch triển khai giáo trình AI Engineer Roadmap

## 1. Phạm vi của lượt triển khai này

Tài liệu này ghi kế hoạch triển khai trước khi viết lại nội dung chi tiết cho 6 tháng.

Trong lượt hiện tại chỉ thực hiện:

- Đọc tài liệu nền của repository.
- Kiểm tra cấu trúc thư mục và mức độ hoàn thiện hiện tại.
- Xác định nội dung còn thiếu, điểm mâu thuẫn và rủi ro quá tải.
- Lập kế hoạch triển khai theo từng tháng.

Không thực hiện trong lượt hiện tại:

- Không viết toàn bộ giáo trình chi tiết.
- Không thay thế nội dung các file tuần.
- Không tạo code project `ai-assistant-platform`.
- Không tạo link tài liệu mới nếu chưa kiểm tra.

## 2. Tài liệu đã đọc

- `README.md`
- `00-Prerequisites.md`
- `ROADMAP_SPEC.md`
- `AGENTS.md`
- `VALIDATION.md`
- Một số file mẫu trong các thư mục `Month-01` đến `Month-06`
- `References.md`

Ghi chú: `ROADMAP_SPEC.md`, `AGENTS.md` và `VALIDATION.md` đang hiển thị lỗi encoding khi đọc bằng terminal. Nội dung chính vẫn nhận diện được, nhưng nên chuẩn hóa encoding về UTF-8 trong một lượt riêng để tránh lỗi hiển thị tiếng Việt về sau.

## 3. Hiện trạng repository

Repository hiện có:

```text
.
├── 00-Prerequisites.md
├── AGENTS.md
├── README.md
├── References.md
├── ROADMAP_SPEC.md
├── VALIDATION.md
├── Month-01/
├── Month-02/
├── Month-03/
├── Month-04/
├── Month-05/
└── Month-06/
```

Mỗi thư mục tháng hiện có:

- `README.md`
- `Week-01.md`
- `Week-02.md`
- `Week-03.md`
- `Week-04.md`

Các phần đang thiếu ở cấp tháng:

- `REVIEW.md`
- `RESOURCES.md`

Các phần đang thiếu ở cấp repository:

- `FINAL_REVIEW.md`
- Script hoặc checklist validation tự động nếu muốn kiểm tra lặp lại.
- README chính chưa có hướng dẫn sử dụng roadmap và link đầy đủ tới từng tháng.
- Thư mục project `ai-assistant-platform` chưa tồn tại trong repository hiện tại.

Ghi chú kỹ thuật: lệnh `git status --short` báo `fatal: not a git repository`, nên hiện chưa thể kiểm tra thay đổi bằng Git trong workspace này.

## 4. Vấn đề và mâu thuẫn cần xử lý

### 4.1 Nội dung hiện tại còn là template

Các file tuần hiện có các mục rất chung như:

- `Learn one focused topic`
- `Read official documentation`
- `Implement today's feature`
- `Code runs`

Điều này mâu thuẫn trực tiếp với yêu cầu trong `ROADMAP_SPEC.md`, `VALIDATION.md` và yêu cầu mới nhất của người dùng vì mỗi ngày phải có mục tiêu, tài liệu, bài thực hành, file dự kiến sửa, lệnh chạy, kết quả mong đợi và câu hỏi tự kiểm tra cụ thể.

### 4.2 Ngôn ngữ chưa thống nhất

Nhiều file hiện đang dùng tiếng Anh ngắn gọn. Yêu cầu mới nhất quy định toàn bộ nội dung phải bằng tiếng Việt có dấu, giữ thuật ngữ kỹ thuật tiếng Anh khi phù hợp.

### 4.3 Thiếu `REVIEW.md` và `RESOURCES.md`

`ROADMAP_SPEC.md` yêu cầu mỗi tháng có:

- `README.md`
- `Week-01.md` đến `Week-04.md`
- `REVIEW.md`
- `RESOURCES.md`

Hiện tất cả tháng đều thiếu `REVIEW.md` và `RESOURCES.md`.

### 4.4 Chưa có project thật để phát triển xuyên suốt

Yêu cầu roadmap xoay quanh một project duy nhất là `ai-assistant-platform`. Hiện repository mới có tài liệu Markdown, chưa có thư mục hoặc skeleton project.

Đề xuất xử lý:

- Giai đoạn viết giáo trình: mô tả rõ project progression theo từng ngày.
- Giai đoạn sau khi bạn duyệt kế hoạch: cân nhắc tạo skeleton project tối thiểu ở Month 1 hoặc một lượt riêng, tùy bạn muốn repository này chỉ chứa giáo trình hay vừa chứa giáo trình vừa chứa project mẫu.

### 4.5 Tài liệu tham khảo còn quá chung

`References.md` hiện chủ yếu trỏ tới homepage hoặc trang tổng quan. Quy định yêu cầu mỗi tuần có nguồn chính thức hoặc uy tín, ghi rõ phần cần đọc, không tự bịa URL.

Đề xuất xử lý:

- Mỗi `RESOURCES.md` tháng gom nguồn chính.
- Mỗi file tuần chỉ chọn tối đa 3-5 nguồn bắt buộc.
- Nếu chưa xác minh đường dẫn, ghi `Cần xác minh` thay vì tạo URL giả.

### 4.6 Evaluation cần xuất hiện sớm hơn production

Yêu cầu đã rõ: evaluation bắt đầu từ tháng 3-4, không đợi tháng 6.

Đề xuất xử lý:

- Tháng 3: prompt regression test, schema validation, tool result test.
- Tháng 4: RAG evaluation dataset, baseline retrieval, RAGAS hoặc DeepEval.
- Tháng 5: agent evaluation, failure taxonomy, trace review.
- Tháng 6: quality regression chạy trong CI hoặc runbook.

## 5. Nguyên tắc triển khai nội dung

Khi bắt đầu viết chi tiết, mỗi tuần phải có:

1. Mục tiêu tuần.
2. Kiến thức cần đạt.
3. Kiến trúc hoặc tính năng project sẽ bổ sung.
4. Kế hoạch từng ngày.
5. Milestone cuối tuần.
6. Review checklist.
7. Definition of Done.
8. Những lỗi thường gặp.
9. Tài liệu tham khảo chính thức.
10. Nội dung tùy chọn nếu còn thời gian.

Mỗi ngày phải có:

1. Mục tiêu cụ thể.
2. Kết quả cần đạt.
3. Phân bổ thời gian 1-2 giờ.
4. Nội dung lý thuyết.
5. Tài liệu cần đọc.
6. Bài thực hành.
7. Thay đổi cần áp dụng vào `ai-assistant-platform`.
8. File dự kiến tạo hoặc sửa.
9. Lệnh cần chạy.
10. Kết quả mong đợi.
11. Cách kiểm tra kết quả.
12. Definition of Done.
13. Commit message gợi ý.
14. Câu hỏi tự kiểm tra.

Mẫu thời lượng mặc định:

- 10 phút: ôn lại ngày trước.
- 20-30 phút: lý thuyết.
- 40-50 phút: thực hành.
- 15-25 phút: tích hợp project.
- 10 phút: ghi chú, commit và tự kiểm tra.

Ngày milestone tối đa 120 phút. Ngày review hoặc buffer khoảng 60-90 phút.

## 6. Kế hoạch triển khai theo tháng

### Tháng 1: Python, uv, FastAPI, Docker và PyTorch inference cơ bản

Mục tiêu triển khai:

- Chuyển người học từ tư duy backend PHP/NestJS sang Python backend.
- Không học lại REST API quá sâu.
- Tạo nền project `ai-assistant-platform` với FastAPI, Pydantic, config, logging, test, Docker.
- Kết thúc tháng bằng inference endpoint PyTorch đơn giản.

Kế hoạch 4 tuần:

- Tuần 1: Python thiết yếu cho backend, type hint, dataclass, exception, logging, JSON, pathlib, `uv`.
- Tuần 2: FastAPI, router, Pydantic request/response, dependency injection, config, middleware, error handling.
- Tuần 3: async/await, `httpx`, Dockerfile, Docker Compose, env var, health check, logging chuẩn, unit test.
- Tuần 4: PyTorch Tensor, shape, dtype, Dataset/DataLoader overview, load model có sẵn, inference endpoint.

Deliverable cần đạt:

- FastAPI service chạy được.
- `GET /health`.
- `POST /api/v1/chat` mock response.
- Config từ `.env.example`.
- Dockerfile và Docker Compose.
- Test cơ bản.
- PyTorch inference demo.

### Tháng 2: Data processing, ML foundation, Neural Network và Transformer foundation

Mục tiêu triển khai:

- Giảm Machine Learning cổ điển, chỉ học đủ để hiểu training, evaluation và dữ liệu.
- Tập trung data processing, classification metrics, PyTorch training loop, embedding và Transformer foundation.
- Tạo module preprocessing có thể tái sử dụng trong project chính.

Kế hoạch 4 tuần:

- Tuần 1: NumPy, pandas, CSV/JSON, missing values, encoding, scaling, train/validation/test split, data leakage.
- Tuần 2: supervised learning, Linear Regression ở mức nền tảng, Logistic Regression, confusion matrix, precision, recall, F1.
- Tuần 3: PyTorch Dataset, DataLoader, Neural Network, activation, loss, optimizer, training loop, validation loop.
- Tuần 4: tokenization, embedding, attention, self-attention, multi-head attention, positional encoding, Transformer overview.

Deliverable cần đạt:

- Data pipeline nhỏ.
- Classification model cơ bản.
- Script hoặc notebook training.
- Evaluation report cho model cơ bản.
- Tài liệu giải thích Transformer bằng lời của người học.
- Module preprocessing dùng lại được.

### Tháng 3: LLM Engineering, Structured Output, Tool Calling và MCP

Mục tiêu triển khai:

- Tích hợp LLM thật vào `ai-assistant-platform`.
- Dùng Structured Output bằng Pydantic.
- Xây Tool Calling có giới hạn, timeout, retry và error handling.
- Tạo MCP Server đơn giản.
- Bắt đầu evaluation cho LLM workflow.

Kế hoạch 4 tuần:

- Tuần 1: OpenAI SDK, Responses API, message roles, model configuration, streaming, token usage, cost awareness, retry, timeout.
- Tuần 2: prompt structure, system instruction, few-shot prompting, Structured Output, Pydantic validation, fallback khi output lỗi, prompt regression test.
- Tuần 3: tool schema, tool execution, tool result, tool error, timeout, retry, tool budget, giới hạn vòng lặp.
- Tuần 4: MCP overview, MCP Server, tool, resource, client concept, security boundary.

Deliverable cần đạt:

- `POST /api/v1/chat` gọi LLM thật.
- Streaming response.
- Structured Output endpoint hoặc service.
- Ít nhất hai tool an toàn.
- MCP Server đơn giản.
- Prompt regression tests.
- Logging usage, latency và error.

### Tháng 4: RAG, hybrid retrieval, reranking, citation và evaluation

Mục tiêu triển khai:

- Xây RAG có ingestion, chunking, metadata, Qdrant, BM25, Hybrid Search, reranking, query rewriting và citation.
- Có evaluation dataset và baseline từ đầu.
- Không dừng ở vector search đơn giản.

Kế hoạch 4 tuần:

- Tuần 1: document ingestion, file parsing, chunking strategy, metadata, document ID, versioning, deduplication.
- Tuần 2: embedding, Qdrant collection, payload, filtering, top-k, dense retrieval, BM25, sparse retrieval, Hybrid Search.
- Tuần 3: query rewriting, multi-query overview, reranking, context compression, citation, source attribution, từ chối trả lời khi thiếu căn cứ, prompt injection trong tài liệu.
- Tuần 4: golden questions, faithfulness, answer relevancy, context precision, context recall, RAGAS, DeepEval, latency, cost, error analysis.

Deliverable cần đạt:

- Upload hoặc ingest tài liệu.
- Qdrant collection.
- Dense retrieval, BM25 và Hybrid Search.
- Reranking.
- Citation trong câu trả lời.
- RAG evaluation dataset.
- Evaluation report so sánh ít nhất hai cấu hình retrieval.

### Tháng 5: LangGraph Agent, reliability và human-in-the-loop

Mục tiêu triển khai:

- Phân biệt rõ Tool Calling và Agent.
- Xây workflow LangGraph có state, node, edge, conditional routing.
- Có checkpoint, persistence, memory, human approval, guardrails, retry, timeout và max steps.
- Có agent evaluation.

Kế hoạch 4 tuần:

- Tuần 1: agent fundamentals, state, node, edge, conditional routing, deterministic workflow, khi nào không nên dùng agent.
- Tuần 2: LangGraph checkpoint, persistence, conversation state, short-term memory, long-term memory overview, Redis/PostgreSQL persistence.
- Tuần 3: human-in-the-loop, approval step, interrupt/resume, retry, timeout, tool budget, max steps, idempotency, error recovery.
- Tuần 4: guardrails, input/output validation, prompt injection defense, permission boundary, LangSmith tracing, agent evaluation, failure taxonomy, cost và latency budget.

Deliverable cần đạt:

- LangGraph workflow nhiều bước.
- State persistence.
- Human approval cho hành động nhạy cảm.
- Retry, timeout, max steps và tool budget.
- Guardrails cơ bản.
- LangSmith tracing.
- Agent evaluation report.

### Tháng 6: Production, AWS deployment, CI/CD, monitoring và MLOps cơ bản

Mục tiêu triển khai:

- Đưa hệ thống lên môi trường demo hợp lý bằng Docker và AWS EC2.
- Có CI/CD bằng GitHub Actions.
- Có monitoring, tracing, logging, quality regression và runbook.
- Chỉ học Ollama/vLLM ở mức overview, không đổi trọng tâm stack.

Kế hoạch 4 tuần:

- Tuần 1: production config, secret management, Docker image, multi-stage build, health/readiness check, logging format, rate limiting, security headers, dependency vulnerability check.
- Tuần 2: AWS EC2, security group overview, Docker deployment, Nginx, HTTPS, domain overview, persistent storage, backup, rollback.
- Tuần 3: GitHub Actions, lint, type check, unit test, integration test, build image, deploy workflow, environment protection, release checklist.
- Tuần 4: metrics, latency, error rate, token usage, cost, LangSmith tracing, quality regression, scheduled RAG/Agent evaluation, final demo, portfolio README, ADR.

Deliverable cần đạt:

- Ứng dụng deploy được.
- HTTPS hoặc hướng dẫn cấu hình HTTPS rõ ràng.
- CI/CD pipeline.
- Monitoring và tracing.
- Quality evaluation pipeline.
- Runbook vận hành.
- Architecture document.
- Demo script và portfolio README.

## 7. Thứ tự triển khai đề xuất sau khi kế hoạch được duyệt

### Giai đoạn 1: Chuẩn hóa khung repository

1. Cập nhật README chính để mô tả cách dùng roadmap và link tới 6 tháng.
2. Tạo `REVIEW.md` và `RESOURCES.md` cho từng tháng.
3. Chuẩn hóa README của từng tháng theo cấu trúc trong `ROADMAP_SPEC.md`.
4. Sửa lỗi encoding nếu bạn xác nhận muốn xử lý trong cùng repository.

### Giai đoạn 2: Viết chi tiết Month 1

1. Viết `Month-01/README.md`.
2. Viết `Month-01/Week-01.md` đến `Week-04.md`.
3. Viết `Month-01/RESOURCES.md`.
4. Viết `Month-01/REVIEW.md`.
5. Đối chiếu với `VALIDATION.md`.

Lý do bắt đầu từ Month 1: các tháng sau phụ thuộc vào cấu trúc project, command, naming và convention được thiết lập ở tháng đầu.

### Giai đoạn 3: Viết lần lượt Month 2 đến Month 6

Mỗi tháng chỉ bắt đầu sau khi tháng trước đã có:

- README tháng.
- 4 tuần đủ 7 ngày.
- Milestone tuần.
- Review checklist.
- Definition of Done.
- Resource file.
- Validation report hoặc review notes.

### Giai đoạn 4: Validation toàn repository

1. Kiểm tra đủ 6 tháng, 24 tuần và 168 ngày học.
2. Kiểm tra ngày học không vượt 120 phút bắt buộc.
3. Kiểm tra không còn placeholder.
4. Kiểm tra internal links.
5. Kiểm tra tài liệu tham khảo.
6. Kiểm tra evaluation xuất hiện từ tháng 3-4.
7. Kiểm tra project progression xuyên suốt.
8. Tạo `FINAL_REVIEW.md`.

## 8. Chiến lược tài liệu tham khảo

Nguồn ưu tiên:

- Official Python documentation.
- Official uv documentation.
- Official FastAPI documentation.
- Official Pydantic documentation.
- Official PyTorch tutorials.
- Official OpenAI platform documentation.
- Official Qdrant documentation.
- Official LangGraph documentation.
- Official RAGAS documentation.
- Official DeepEval documentation.
- Official LangSmith documentation.
- Official Docker documentation.
- Official GitHub Actions documentation.
- Official AWS documentation.

Quy tắc khi viết chi tiết:

- Không tự tạo URL theo suy đoán.
- Không chỉ ghi homepage nếu có trang tutorial hoặc concept cụ thể phù hợp hơn.
- Mỗi tuần giới hạn khoảng 3-5 nguồn bắt buộc.
- Ghi rõ phần cần đọc, ví dụ: section về Request Body, Pydantic Models, Docker Compose services.
- Nếu chưa xác minh được, ghi `Cần xác minh trước khi xuất bản`.

## 9. Rủi ro quá tải và cách giảm tải

Rủi ro chính:

- Tháng 2 dễ biến thành roadmap Data Scientist nếu học quá sâu ML cổ điển.
- Tháng 4 có nhiều nội dung retrieval nâng cao, cần chia nhỏ để không vượt 2 giờ/ngày.
- Tháng 5 có thể quá tải nếu vừa học LangGraph vừa thêm quá nhiều tool phức tạp.
- Tháng 6 có thể quá rộng nếu đi sâu AWS, Nginx, CI/CD, monitoring và MLOps cùng lúc.

Cách giảm tải:

- Giữ mỗi ngày một trọng tâm chính.
- Đưa nội dung nâng cao vào `Tìm hiểu thêm`.
- Không bắt buộc học framework thay thế.
- Không yêu cầu Kubernetes, local model serving nâng cao hoặc MLOps chuyên sâu.
- Milestone chỉ tổng hợp các phần đã học trong tuần, không thêm chủ đề lớn mới.

## 10. Tiêu chí chấp nhận trước khi viết giáo trình chi tiết

Kế hoạch này nên được review theo các câu hỏi:

1. Thứ tự 6 tháng đã đúng với mục tiêu GenAI/LLM chưa?
2. Tháng 2 đã đủ nền tảng nhưng không quá nghiêng về Data Science chưa?
3. Evaluation xuất hiện đủ sớm từ tháng 3-4 chưa?
4. Project `ai-assistant-platform` nên chỉ được mô tả trong giáo trình hay cũng cần tạo skeleton code trong repository này?
5. Có muốn xử lý lỗi encoding của các file đặc tả trước khi viết nội dung chi tiết không?
6. Có muốn viết lần lượt từng tháng để review, hay viết từng tuần để review chặt hơn?

## 11. Đề xuất bước tiếp theo

Sau khi bạn review `IMPLEMENTATION_PLAN.md`, bước tiếp theo nên là một trong hai hướng:

- Hướng A: Chuẩn hóa khung repository trước, gồm README chính, README từng tháng, `REVIEW.md`, `RESOURCES.md`.
- Hướng B: Viết chi tiết Month 1 trước, sau đó dùng Month 1 làm mẫu chất lượng cho các tháng còn lại.

Đề xuất của tôi là chọn Hướng B nếu mục tiêu là nhanh có nội dung học được, và chọn Hướng A nếu mục tiêu là làm repository sạch cấu trúc trước.
