# ROADMAP_SPEC.md

## 1. Mục đích tài liệu

Tài liệu này là đặc tả nguồn cho bộ giáo trình tự học **AI Engineer thiên về GenAI/LLM trong 6 tháng**.

Bộ giáo trình phải được triển khai dưới dạng nhiều file Markdown, chia theo:

- Tháng.
- Tuần.
- Ngày.
- Milestone.
- Review.
- Definition of Done.

Mục tiêu không phải tạo một danh sách chủ đề, mà tạo một **playbook học tập có thể thực thi hằng ngày**.

---

## 2. Đối tượng người học

Người học đã có nền tảng kỹ thuật sau:

- Đã làm việc với PHP, ReactJS và NestJS.
- Có kiến thức về REST API và backend development.
- Đã sử dụng Git và GitHub.
- Đã sử dụng Docker.
- Có kiến thức AWS và AWS CDK cơ bản.
- Chưa coi Ollama hoặc Local LLM là kiến thức đã có.
- Có thể học khoảng 1–2 giờ mỗi ngày.
- Có khả năng đọc tài liệu kỹ thuật bằng tiếng Anh ở mức cơ bản đến trung bình.

Do đó, giáo trình không được dành quá nhiều thời gian cho:

- REST API cơ bản.
- Git cơ bản.
- Docker cơ bản.
- SQL cơ bản.
- Kiến trúc backend nhập môn.
- JavaScript hoặc TypeScript cơ bản.

Các nội dung này chỉ được ôn lại khi cần để phục vụ project.

---

## 3. Mục tiêu sau 6 tháng

Sau khi hoàn thành roadmap, người học phải có khả năng:

1. Viết Python đủ tốt để xây dựng AI backend.
2. Xây dựng API AI bằng FastAPI.
3. Dùng `uv` để quản lý môi trường và dependency.
4. Hiểu nền tảng Machine Learning, Neural Network và Transformer.
5. Tích hợp LLM API vào sản phẩm.
6. Dùng Pydantic để tạo Structured Output.
7. Xây dựng Tool Calling và MCP Server đơn giản.
8. Xây dựng hệ thống RAG có:
   - Chunking.
   - Metadata.
   - Dense retrieval.
   - BM25.
   - Hybrid Search.
   - Reranking.
   - Query rewriting.
   - Citation.
   - Evaluation.
9. Xây dựng Agent bằng LangGraph có:
   - State.
   - Persistence.
   - Checkpoint.
   - Memory.
   - Human-in-the-loop.
   - Retry.
   - Timeout.
   - Guardrails.
   - Observability.
10. Triển khai hệ thống AI lên AWS bằng Docker.
11. Thiết lập CI/CD, logging, monitoring và tracing cơ bản.
12. Có một repository portfolio hoàn chỉnh, có thể demo và giải thích trong phỏng vấn.

---

## 4. Nguyên tắc thiết kế roadmap

### 4.1 Một project xuyên suốt

Toàn bộ 6 tháng phải xoay quanh một project duy nhất:

```text
ai-assistant-platform
```

Project này được mở rộng dần qua từng tháng.

Không tạo sáu project rời rạc.

Mini project chỉ được phép tồn tại như:

- Module thử nghiệm.
- Notebook thực hành.
- Spike kỹ thuật.
- Feature branch.
- Bài tập bổ trợ được tích hợp lại vào project chính.

### 4.2 Project-based learning

Tỷ lệ thời gian khuyến nghị:

- 30% lý thuyết.
- 70% thực hành.

Mỗi ngày phải có một thay đổi cụ thể áp dụng vào project hoặc một bài thực hành có đầu ra đo được.

### 4.3 Không nhồi quá nhiều công cụ

Phần học chính chỉ sử dụng một stack thống nhất.

Các framework hoặc công cụ thay thế chỉ được đưa vào mục:

```text
Tìm hiểu thêm
```

Không được làm người học phân tán bằng cách yêu cầu học nhiều framework tương đương.

### 4.4 Evaluation học sớm

Evaluation không được để đến tháng 6 mới học.

Evaluation phải xuất hiện theo tiến trình:

- Tháng 3: kiểm tra Structured Output, tool result và regression test cho prompt.
- Tháng 4: RAG Evaluation.
- Tháng 5: Agent Evaluation.
- Tháng 6: Production monitoring và quality regression.

### 4.5 Production mindset xuyên suốt

Các chủ đề sau phải được đưa vào ngay khi phù hợp:

- Error handling.
- Logging.
- Timeout.
- Retry.
- Validation.
- Security.
- Prompt injection.
- Cost.
- Latency.
- Testability.
- Observability.

---

## 5. Main stack

| Thành phần | Công nghệ chính |
|---|---|
| Ngôn ngữ | Python |
| Package manager | uv |
| API | FastAPI |
| Validation | Pydantic |
| ML/DL | scikit-learn, PyTorch |
| LLM API | OpenAI API |
| Database | PostgreSQL |
| Vector database | Qdrant |
| Cache / transient state | Redis |
| Agent orchestration | LangGraph |
| RAG evaluation | RAGAS |
| LLM/Agent evaluation | DeepEval |
| Observability | LangSmith |
| Container | Docker, Docker Compose |
| CI/CD | GitHub Actions |
| Cloud | AWS EC2 |
| Reverse proxy | Nginx |
| Source control | Git, GitHub |

### Công cụ chỉ học ở mức overview hoặc tùy chọn

- Ollama.
- vLLM.
- SGLang.
- MLflow.
- Arize Phoenix.
- pgvector.
- Weights & Biases.
- Kubernetes.
- TensorRT.
- ONNX.
- DVC.

Các công cụ này không được làm thay đổi trọng tâm roadmap chính.

---

## 6. Kiến trúc project mục tiêu

```text
ai-assistant-platform/
├── app/
│   ├── api/
│   ├── core/
│   ├── domain/
│   ├── services/
│   ├── llm/
│   ├── rag/
│   ├── agents/
│   ├── evaluation/
│   ├── observability/
│   └── main.py
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── evaluation/
│   └── fixtures/
├── scripts/
├── notebooks/
├── docs/
├── infra/
├── .github/workflows/
├── pyproject.toml
├── uv.lock
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```

Cấu trúc trên là đích đến cuối tháng 6. Không bắt buộc phải xuất hiện đầy đủ từ tháng 1.

---

## 7. Kế hoạch 6 tháng

# Tháng 1 — Python, FastAPI, Docker và PyTorch cơ bản

## Mục tiêu tháng

- Chuyển từ tư duy backend JavaScript/TypeScript sang Python.
- Xây dựng FastAPI service có cấu trúc.
- Quản lý dependency bằng `uv`.
- Chạy ứng dụng bằng Docker.
- Hiểu Tensor và inference cơ bản bằng PyTorch.
- Tạo nền móng cho `ai-assistant-platform`.

## Nội dung chính

### Tuần 1
- Python syntax cần thiết cho backend.
- Function.
- Type hint.
- Dataclass.
- OOP.
- Exception.
- Logging.
- File I/O.
- JSON.
- pathlib.
- Virtual environment và `uv`.

### Tuần 2
- FastAPI.
- Router.
- Request/response model.
- Pydantic.
- Dependency Injection.
- Configuration.
- Middleware.
- Error handling.
- OpenAPI docs.

### Tuần 3
- Async/await.
- HTTP client bằng `httpx`.
- Dockerfile.
- Docker Compose.
- Environment variables.
- Health check.
- Logging chuẩn.
- Unit test cơ bản.

### Tuần 4
- PyTorch Tensor.
- Shape.
- dtype.
- CPU/GPU concept.
- Dataset/DataLoader overview.
- Load model có sẵn.
- Inference.
- Tích hợp một inference endpoint đơn giản.

## Deliverable tháng 1

- FastAPI project chạy được.
- Có `POST /chat` trả fake response hoặc mock response.
- Có `/health`.
- Có config từ `.env`.
- Có Dockerfile và Docker Compose.
- Có logging.
- Có test cơ bản.
- Có demo PyTorch inference.
- Có README hướng dẫn chạy.

---

# Tháng 2 — Data Processing, ML Foundation, Neural Network và Transformer

## Mục tiêu tháng

- Hiểu quy trình dữ liệu và Machine Learning.
- Không học sâu quá nhiều thuật toán cổ điển.
- Hiểu Neural Network, Embedding và Transformer foundation.
- Biết cách đánh giá một model classification cơ bản.

## Nội dung chính

### Tuần 1
- NumPy.
- pandas.
- CSV.
- JSON.
- Parquet overview.
- Missing values.
- Encoding.
- Scaling.
- Train/validation/test split.
- Data leakage.

### Tuần 2
- Supervised learning.
- Regression overview.
- Classification.
- Linear Regression.
- Logistic Regression.
- Confusion Matrix.
- Precision.
- Recall.
- F1.
- ROC-AUC overview.

### Tuần 3
- Tensor.
- Dataset.
- DataLoader.
- Neural Network.
- Activation.
- Loss.
- Optimizer.
- Backpropagation.
- Training loop.
- Validation loop.

### Tuần 4
- Tokenization.
- Embedding.
- Attention.
- Self-attention.
- Multi-head attention.
- Positional encoding.
- Transformer encoder/decoder.
- Vì sao LLM dự đoán token tiếp theo.

## Nội dung không được học quá sâu

- SVM.
- KNN.
- PCA.
- Naive Bayes.
- Random Forest tuning.
- XGBoost tuning.
- Mathematical proof của backpropagation.
- Tự code Transformer hoàn chỉnh từ đầu.

## Deliverable tháng 2

- Có data pipeline nhỏ.
- Có classification model cơ bản.
- Có notebook hoặc script training.
- Có model evaluation report.
- Có tài liệu giải thích Transformer bằng lời của người học.
- Có module preprocessing có thể tái sử dụng trong project chính.

---

# Tháng 3 — LLM Engineering, Structured Output, Tool Calling và MCP

## Mục tiêu tháng

- Tích hợp LLM thật vào project.
- Xây dựng output có cấu trúc.
- Dùng tool an toàn.
- Tạo MCP Server đơn giản.
- Bắt đầu evaluation cho LLM workflow.

## Nội dung chính

### Tuần 1
- OpenAI SDK.
- Responses API.
- Message roles.
- Model configuration.
- Streaming.
- Token usage.
- Cost awareness.
- Error handling.
- Retry và timeout.

### Tuần 2
- Prompt structure.
- System instruction.
- Few-shot prompting.
- Prompt templates.
- Structured Output.
- Pydantic model.
- Validation.
- Fallback khi output lỗi.
- Prompt regression test.

### Tuần 3
- Function Calling.
- Tool schema.
- Tool selection.
- Tool execution.
- Tool result.
- Tool error.
- Timeout.
- Retry.
- Tool budget.
- Không để model gọi tool vô hạn.

### Tuần 4
- MCP overview.
- MCP Server.
- Tool.
- Resource.
- Client concept.
- Tạo MCP Server đơn giản.
- Security boundary của MCP.

## Deliverable tháng 3

- `POST /chat` gọi được LLM.
- Có streaming.
- Có Structured Output.
- Có ít nhất hai tool.
- Có MCP Server đơn giản.
- Có test cho Pydantic schema.
- Có bộ prompt regression nhỏ.
- Có logging usage, latency và error.

---

# Tháng 4 — RAG nâng cao và Evaluation

## Mục tiêu tháng

- Xây dựng RAG có thể giải thích được.
- Không dừng ở embedding + vector database.
- Có citation và evaluation.
- Hiểu các quyết định thiết kế retrieval.

## Nội dung chính

### Tuần 1
- Document ingestion.
- File parsing.
- Chunking strategy.
- Chunk size.
- Chunk overlap.
- Semantic chunking overview.
- Metadata.
- Document ID.
- Versioning.
- Deduplication.

### Tuần 2
- Embedding.
- Qdrant.
- Collection.
- Payload.
- Filtering.
- Top-k.
- Dense retrieval.
- BM25.
- Sparse retrieval.
- Hybrid Search.

### Tuần 3
- Query rewriting.
- Multi-query retrieval overview.
- Reranking.
- Cross-encoder concept.
- Context compression.
- Citation.
- Source attribution.
- Không trả lời khi thiếu căn cứ.
- Prompt injection trong tài liệu.

### Tuần 4
- RAG evaluation dataset.
- Golden questions.
- Faithfulness.
- Answer relevancy.
- Context precision.
- Context recall.
- RAGAS.
- DeepEval.
- Latency.
- Cost.
- Error analysis.

## Deliverable tháng 4

- Upload tài liệu.
- Ingestion pipeline.
- Qdrant collection.
- Dense + BM25 + Hybrid Search.
- Reranking.
- Citation.
- RAG evaluation dataset.
- Evaluation report.
- So sánh ít nhất hai cấu hình retrieval.

---

# Tháng 5 — LangGraph Agent, Reliability và Human-in-the-loop

## Mục tiêu tháng

- Xây dựng workflow agent có kiểm soát.
- Phân biệt rõ Tool Calling với Agent.
- Có state, persistence, approval và guardrails.
- Có evaluation cho workflow nhiều bước.

## Nội dung chính

### Tuần 1
- Agent fundamentals.
- State.
- Node.
- Edge.
- Conditional routing.
- Deterministic workflow.
- Khi nào không nên dùng agent.

### Tuần 2
- LangGraph.
- Checkpoint.
- Persistence.
- Conversation state.
- Short-term memory.
- Long-term memory overview.
- Redis/PostgreSQL persistence.

### Tuần 3
- Human-in-the-loop.
- Approval step.
- Interrupt/resume.
- Retry.
- Timeout.
- Tool budget.
- Max steps.
- Idempotency.
- Error recovery.

### Tuần 4
- Guardrails.
- Input validation.
- Output validation.
- Prompt injection defense.
- Permission boundary.
- LangSmith tracing.
- Agent evaluation.
- Failure taxonomy.
- Cost và latency budget.

## Deliverable tháng 5

- LangGraph workflow nhiều bước.
- Có state persistence.
- Có human approval.
- Có retry và timeout.
- Có giới hạn số bước và tool budget.
- Có guardrails cơ bản.
- Có tracing.
- Có agent evaluation report.

---

# Tháng 6 — Production, Cloud, CI/CD, Observability và MLOps cơ bản

## Mục tiêu tháng

- Đưa hệ thống lên môi trường có thể demo.
- Có CI/CD.
- Có monitoring.
- Có tài liệu vận hành.
- Biết giới hạn và trade-off của local model serving.

## Nội dung chính

### Tuần 1
- Production config.
- Secret management.
- Docker image.
- Multi-stage build.
- Health check.
- Readiness.
- Logging format.
- Rate limiting.
- Security headers.
- Dependency vulnerability check.

### Tuần 2
- AWS EC2.
- VPC/security group overview.
- Docker deployment.
- Nginx.
- HTTPS.
- Domain overview.
- Persistent storage.
- Backup cơ bản.
- Rollback.

### Tuần 3
- GitHub Actions.
- Lint.
- Type check.
- Unit test.
- Integration test.
- Build image.
- Deploy workflow.
- Environment protection.
- Release checklist.

### Tuần 4
- Metrics.
- Latency.
- Error rate.
- Token usage.
- Cost.
- LangSmith tracing.
- Quality regression.
- RAG/Agent evaluation chạy định kỳ.
- MLflow overview.
- Ollama/vLLM overview.
- Final demo.
- Portfolio README.
- Architecture Decision Records.

## Deliverable tháng 6

- Ứng dụng được deploy.
- Có HTTPS.
- Có CI/CD.
- Có monitoring và tracing.
- Có test pipeline.
- Có quality evaluation pipeline.
- Có runbook.
- Có architecture document.
- Có demo script.
- Có portfolio README.

---

## 8. Cấu trúc mỗi tháng

Mỗi thư mục tháng phải có:

```text
Month-XX/
├── README.md
├── Week-01.md
├── Week-02.md
├── Week-03.md
├── Week-04.md
├── REVIEW.md
└── RESOURCES.md
```

`README.md` của tháng phải có:

1. Mục tiêu tháng.
2. Kiến thức đầu vào.
3. Kết quả đầu ra.
4. Kiến trúc trước và sau tháng.
5. Milestone từng tuần.
6. Definition of Done tháng.
7. Rủi ro quá tải.
8. Nội dung được phép bỏ qua nếu thiếu thời gian.

---

## 9. Cấu trúc mỗi tuần

Mỗi file tuần phải có:

1. Mục tiêu tuần.
2. Kiến thức cần đạt.
3. Feature hoặc module sẽ bổ sung.
4. Kế hoạch từng ngày.
5. Milestone cuối tuần.
6. Review checklist.
7. Definition of Done.
8. Lỗi thường gặp.
9. Tài liệu chính thức.
10. Nội dung tùy chọn nếu còn thời gian.

---

## 10. Cấu trúc mỗi ngày

Mỗi ngày phải có đầy đủ:

1. **Mục tiêu cụ thể.**
2. **Kết quả cần đạt.**
3. **Phân bổ thời gian 1–2 giờ.**
4. **Lý thuyết cần học.**
5. **Tài liệu cần đọc.**
6. **Bài thực hành.**
7. **Thay đổi trong project.**
8. **File dự kiến tạo hoặc sửa.**
9. **Lệnh cần chạy.**
10. **Kết quả mong đợi.**
11. **Cách tự kiểm tra.**
12. **Definition of Done.**
13. **Commit message gợi ý.**
14. **2–5 câu hỏi tự kiểm tra.**

Không được dùng nội dung mơ hồ như:

- Học Python.
- Tìm hiểu RAG.
- Đọc tài liệu.
- Làm mini project.
- Ôn lại.
- Tiếp tục project.

Mỗi ngày phải chỉ rõ người học làm gì.

---

## 11. Phân bổ thời gian

Mặc định mỗi ngày:

```text
10 phút  — Ôn lại ngày trước
25 phút  — Lý thuyết
45 phút  — Thực hành
20 phút  — Tích hợp project
10 phút  — Ghi chú, commit và tự kiểm tra
```

Có thể điều chỉnh:

- Ngày nhẹ: 60–75 phút.
- Ngày thường: 90 phút.
- Ngày milestone: tối đa 120 phút.
- Ngày review: 60–90 phút.
- Không thiết kế ngày bắt buộc trên 2 giờ.

---

## 12. Chiến lược giảm tải để giữ đúng 6 tháng

Nếu nội dung quá tải, cắt theo thứ tự sau:

1. Công cụ thay thế.
2. Nội dung overview nâng cao.
3. Toán chứng minh.
4. Framework thứ hai.
5. Tối ưu hiệu năng sâu.
6. Local model serving nâng cao.
7. Kubernetes.
8. MLOps chuyên sâu.

Không được cắt:

- Python.
- FastAPI.
- Structured Output.
- Tool Calling.
- RAG.
- Hybrid Search.
- Reranking.
- Evaluation.
- LangGraph state.
- Human-in-the-loop.
- Guardrails.
- CI/CD.
- Monitoring.
- Project integration.

---

## 13. Yêu cầu chất lượng tài liệu

- Viết bằng tiếng Việt.
- Thuật ngữ kỹ thuật giữ tiếng Anh khi cần.
- Không dịch máy cứng nhắc.
- Không quảng cáo.
- Không khẳng định người học chắc chắn có việc sau 6 tháng.
- Không tạo link giả.
- Ưu tiên tài liệu chính thức.
- Mỗi tài liệu phải ghi rõ phần cần đọc, không chỉ ghi tên trang chủ.
- Hạn chế dùng quá nhiều video.
- Mỗi tuần không nên có quá 5 nguồn bắt buộc.
- Không sao chép cùng một template cho mọi ngày mà không cá nhân hóa.
- Không lặp lại Definition of Done chung chung.
- Mỗi tuần phải nối tiếp tuần trước.
- Mỗi tháng phải tạo ra một thay đổi nhìn thấy được trong project.

---

## 14. Tiêu chí hoàn thành toàn roadmap

Roadmap được coi là hoàn chỉnh khi:

- Có đủ 6 tháng.
- Có đủ 24 tuần chính.
- Mỗi tuần có 7 ngày hoặc lịch tương đương được giải thích rõ.
- Không có ngày nào chỉ chứa placeholder.
- Project phát triển liên tục.
- Có internal links hợp lệ.
- Có tài liệu tham khảo.
- Có review file cho từng tháng.
- Có final review.
- Có script hoặc checklist validation.
- Khối lượng phù hợp 1–2 giờ/ngày.
- Không biến thành roadmap Data Scientist hoặc AI Researcher.
- Trọng tâm vẫn là AI Engineer thiên về GenAI/LLM.
