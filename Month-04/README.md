# Tháng 4 - RAG, hybrid retrieval, reranking, citation và evaluation

Tháng này biến chat service có LLM, Structured Output, tool calling và MCP của Month-03 thành `ai-assistant-platform` có thể trả lời dựa trên tài liệu đã được kiểm soát. Mục tiêu không phải là “chat với PDF” thật nhanh, mà là một retrieval pipeline đo được, truy vết được nguồn và biết từ chối khi bằng chứng không đủ.

## Mục tiêu tháng

- Xây ingestion pipeline cho Markdown/TXT với chunk, metadata, document ID, version và deduplication.
- Lưu embedding và payload vào Qdrant; triển khai dense, BM25 và hybrid retrieval.
- Thêm query rewriting, reranking, context budget, citation, từ chối có căn cứ và phòng vệ prompt injection trong tài liệu.
- Tạo golden dataset, baseline và report so sánh ít nhất hai cấu hình retrieval bằng RAGAS hoặc DeepEval.

## Kiến thức đầu vào

- Hoàn thành Month-03: FastAPI, Pydantic, async I/O, logging, test, OpenAI Responses API, Structured Output và giới hạn tool execution.
- Biết JSON, HTTP và Docker Compose cơ bản. Không cần biết database vector, IR hay machine learning retrieval trước đó.
- Dùng `.env` local, giữ `.env.example` không có secret; không upload tài liệu nhạy cảm vào môi trường demo.

## Kết quả đầu ra

- `POST /api/v1/rag/ingest` nhận một danh sách đường dẫn đã được allowlist (không nhận URL tùy ý).
- Qdrant collection có vector, payload metadata, document version và fingerprint để deduplicate.
- `POST /api/v1/rag/search` hỗ trợ dense, BM25 và hybrid; kết quả có score cùng source metadata.
- `POST /api/v1/rag/answer` rewrite query, rerank context, trả citations và `insufficient_evidence` khi cần.
- Dataset evaluation, script chạy lại được, report baseline-vs-hybrid và error analysis.

## Kiến trúc trước và sau tháng

Trước tháng này, `ai-assistant-platform` có FastAPI, schema/config/logging/test/Docker, LLM response có structured output, tool calling an toàn và MCP server đơn giản. Chưa có knowledge base hay đánh giá retrieval.

```text
ai-assistant-platform/
├── app/
│   ├── api/routes/rag.py
│   ├── rag/
│   │   ├── ingestion.py       # parse → normalize → chunk → fingerprint
│   │   ├── schemas.py
│   │   ├── embeddings.py
│   │   ├── qdrant_store.py
│   │   ├── bm25_index.py
│   │   ├── retrieval.py
│   │   ├── reranker.py
│   │   ├── answer_service.py
│   │   └── safety.py
├── data/knowledge_base/        # local, allowlisted corpus demo
├── evals/rag/
│   ├── golden_questions.jsonl
│   ├── run_rag_eval.py
│   └── reports/
├── tests/{unit,integration}/
└── docker-compose.yml          # API + Qdrant
```

## Milestone từng tuần

| Tuần | Trọng tâm | Đầu ra kiểm tra được |
| --- | --- | --- |
| [Tuần 1](./Week-01.md) | Ingestion và chunking | Corpus demo được parse, versioned, deduplicated và có unit test |
| [Tuần 2](./Week-02.md) | Qdrant, dense/BM25/hybrid | API search chạy ba mode và filter metadata |
| [Tuần 3](./Week-03.md) | Rerank, citation và safety | RAG answer có citation, refusal có căn cứ, chống instruction trong document |
| [Tuần 4](./Week-04.md) | Evaluation và demo | Golden dataset, report so sánh hai cấu hình, regression gate |

## Nhịp học và command

Mỗi ngày 60–120 phút: một thay đổi nhỏ, một cách kiểm tra, rồi ghi commit. Lệnh dùng `uv run`; Qdrant local chạy bằng `docker compose up -d qdrant`. Với PowerShell, dùng `$env:QDRANT_URL="http://localhost:6333"` cho biến môi trường tạm thời. Không chạy lệnh xóa collection trong bài học; dùng tên collection theo môi trường, ví dụ `rag_docs_dev`.

## Rủi ro và giảm tải

- Không thêm framework orchestration mới; service Python hiện có gọi Qdrant và LLM trực tiếp.
- Corpus chỉ gồm 3–8 Markdown/TXT công khai hoặc tự viết; parser PDF/OCR là **tùy chọn**.
- Làm BM25 in-memory trước; không thêm Elasticsearch.
- Rerank chỉ lấy top-10 xuống top-4; không fine-tune model.
- Evaluation bắt đầu bằng 10–15 golden questions. Khi thiếu thời gian, chạy DeepEval *hoặc* RAGAS, không bắt buộc cả hai.

## Tài liệu và hoàn thành

Nguồn chính thức, phần cần đọc và link được gom trong [RESOURCES.md](./RESOURCES.md). Xem chi tiết từng ngày ở bốn tuần trên.

### Definition of Done tháng

- Hoàn thành đủ 28 ngày trong [Week-01](./Week-01.md), [Week-02](./Week-02.md), [Week-03](./Week-03.md) và [Week-04](./Week-04.md).
- `uv run pytest` và `uv run ruff check .` pass ở cuối tháng.
- Report có baseline, metric retrieval + generation, threshold, so sánh và lỗi tiêu biểu.
- Câu trả lời RAG chỉ citation những chunk đã retrieve; tài liệu có instruction độc hại không điều khiển prompt.
- Có `docs/month-05-handoff.md` mô tả RAG service để LangGraph dùng như tool ở Month-05.

## Cầu nối sang Month-05

Month-05 sẽ không biến retrieval thành agent tự do. Nó dùng `rag_answer`/`rag_search` đã có citation, timeout và evaluation làm tool có permission boundary trong LangGraph; mọi hành động nhạy cảm vẫn cần human approval.

## Review

Xem [REVIEW.md](./REVIEW.md) để đi tới báo cáo tự review canonical. Review này chỉ xác nhận curriculum và các command/contract dự kiến; source code `ai-assistant-platform` sẽ được kiểm tra bằng chính test suite khi người học triển khai theo lộ trình.
