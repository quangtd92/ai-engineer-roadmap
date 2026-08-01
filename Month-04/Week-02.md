# Tháng 4 - Tuần 2: Qdrant, dense retrieval, BM25 và hybrid search

## Mục tiêu tuần

Đưa chunk tuần 1 vào Qdrant, xây ba retrieval mode đo được và giữ BM25 làm baseline lexical rõ ràng.

## Kiến thức cần đạt

- Vector collection/payload/filter/top-k và khác biệt dense với lexical matching.
- Hybrid fusion không phải concatenate hai list; phải chuẩn hóa/ghi rõ chiến lược.
- Tách interface retrieval để đánh giá công bằng ở tuần 4.

## Tính năng project sẽ bổ sung

Qdrant service trong Compose, `ChunkStore`, embedding adapter, BM25 index và `POST /api/v1/rag/search`.

## Kế hoạch từng ngày

### Ngày 8 - Chạy Qdrant local và cấu hình an toàn

- **Mục tiêu:** Thêm Qdrant vào môi trường local mà không hard-code URL.
- **Kết quả cần đạt:** Service `qdrant` chạy ở port local, `QDRANT_URL`/collection nằm trong settings và `.env.example`.
- **Phân bổ thời gian:** 20 phút đọc, 40 phút Compose/config, 30 phút smoke test, 15 phút ghi chú (105 phút).
- **Lý thuyết:** Collection khác database; development collection không được xóa từ API.
- **Tài liệu:** Qdrant Python Quickstart trong [RESOURCES.md](./RESOURCES.md), Tuần 2.
- **Thực hành:** Thêm health dependency gọi client với timeout ngắn.
- **Tích hợp project:** `docker-compose.yml` có API + Qdrant; config không log URL có credential.
- **File tạo/sửa:** `docker-compose.yml`, `.env.example`, `app/core/config.py`, `app/rag/qdrant_store.py`.
- **Lệnh chạy:** `docker compose up -d qdrant`; `uv run pytest tests/integration/test_qdrant_health.py -q`.
- **Kết quả mong đợi:** Test kết nối local pass hoặc skip có lý do khi Qdrant chưa chạy.
- **Cách kiểm tra:** Mở `http://localhost:6333/healthz`; không đưa endpoint này ra public.
- **Definition of Done:** Qdrant URL chỉ đọc từ config và connection có timeout.
- **Commit message:** `chore(rag): add local qdrant service configuration`
- **Tự kiểm tra:** Vì sao Qdrant không thay thế source document? Khi nào test integration nên skip?

### Ngày 9 - Tạo collection và upsert payload

- **Mục tiêu:** Ghi chunk versioned vào Qdrant với dimension cấu hình rõ ràng.
- **Kết quả cần đạt:** `ensure_collection()` idempotent, `upsert_chunks()` gửi vector+payload và test fake client.
- **Phân bổ thời gian:** 20 phút lý thuyết, 50 phút code, 25 phút test, 15 phút ghi chú (110 phút).
- **Lý thuyết:** Point ID là từ tuần 1; payload dùng filter/citation, không lưu secret.
- **Tài liệu:** Qdrant Points/Payload trong [RESOURCES.md](./RESOURCES.md).
- **Thực hành:** Tạo `QdrantChunkStore` theo protocol `ChunkStore`.
- **Tích hợp project:** Ingestion write path vẫn chỉ nhận corpus allowlist và dùng batch nhỏ.
- **File tạo/sửa:** `app/rag/qdrant_store.py`, `app/rag/store.py`, `tests/unit/test_qdrant_store.py`.
- **Lệnh chạy:** `uv run pytest tests/unit/test_qdrant_store.py -q`.
- **Kết quả mong đợi:** Gọi lại ensure/upsert không tạo collection trùng.
- **Cách kiểm tra:** Assert fake client nhận đúng ID, payload và vector dimension.
- **Definition of Done:** Không tạo collection ở import-time.
- **Commit message:** `feat(rag): add idempotent qdrant chunk store`
- **Tự kiểm tra:** Upsert khác insert ra sao? Payload field nào cần filter index sau này?

### Ngày 10 - Embedding adapter và dense retrieval baseline

- **Mục tiêu:** Đóng gói tạo embedding, không buộc retrieval biết nhà cung cấp model.
- **Kết quả cần đạt:** `Embedder.embed_query/embed_documents`, dense top-k trả `RetrievedChunk` có score.
- **Phân bổ thời gian:** 20 phút đọc, 45 phút adapter/retriever, 30 phút test mock, 15 phút ghi chú (110 phút).
- **Lý thuyết:** Cùng embedding model/dimension cho index và query; cosine score không là xác suất.
- **Tài liệu:** OpenAI Embeddings trong [RESOURCES.md](./RESOURCES.md), Tìm hiểu thêm.
- **Thực hành:** Mock embedder trong test, lưu model name/version ở metadata config.
- **Tích hợp project:** `POST /rag/ingest` chuyển `dry_run=false` chỉ sau explicit config; không cần real key trong test.
- **File tạo/sửa:** `app/rag/embeddings.py`, `app/rag/retrieval.py`, `tests/unit/test_dense_retrieval.py`.
- **Lệnh chạy:** `uv run pytest tests/unit/test_dense_retrieval.py -q`.
- **Kết quả mong đợi:** Query gọi đúng một embedding và trả kết quả giảm dần theo score.
- **Cách kiểm tra:** Fake store trả ba point; assert mapping payload sang schema.
- **Definition of Done:** Adapter có timeout/retry bounded kế thừa policy Month-03, không log query raw.
- **Commit message:** `feat(rag): add dense retrieval behind embedding adapter`
- **Tự kiểm tra:** Vì sao đổi embedding model yêu cầu re-index? Score vector có thể so sánh giữa model không?

### Ngày 11 - BM25 lexical baseline

- **Mục tiêu:** Có retriever lexical độc lập để xử lý exact term và làm baseline.
- **Kết quả cần đạt:** BM25 index từ chunk text, `search(query, k)` và test query có mã lỗi/tên riêng.
- **Phân bổ thời gian:** 20 phút lý thuyết, 45 phút code, 30 phút tests, 15 phút ghi chú (110 phút).
- **Lý thuyết:** Tokenization đơn giản là giới hạn được ghi nhận; BM25 score không cùng thang dense score.
- **Tài liệu:** `rank-bm25` trong [RESOURCES.md](./RESOURCES.md), Tuần 2.
- **Thực hành:** Build index từ chunks sau ingestion, không đọc Qdrant để tạo BM25.
- **Tích hợp project:** Thêm `mode="bm25"` vào request search, giữ metadata/citation contract chung.
- **File tạo/sửa:** `app/rag/bm25_index.py`, `app/rag/schemas.py`, `tests/unit/test_bm25_index.py`.
- **Lệnh chạy:** `uv run pytest tests/unit/test_bm25_index.py -q`.
- **Kết quả mong đợi:** Exact identifier được rank cao hơn paragraph cùng chủ đề nhưng không có identifier.
- **Cách kiểm tra:** Test corpus nhỏ với token hiếm và assert rank 1.
- **Definition of Done:** Index rebuild deterministically từ corpus version, không pickle artifact không rõ nguồn.
- **Commit message:** `feat(rag): add lexical bm25 retrieval baseline`
- **Tự kiểm tra:** BM25 mạnh ở loại query nào? Vì sao không cộng trực tiếp score BM25 và cosine?

### Ngày 12 - Hybrid fusion và metadata filtering

- **Mục tiêu:** Hợp nhất dense/BM25 bằng reciprocal-rank fusion và filter category/version.
- **Kết quả cần đạt:** `mode="hybrid"`, RRF `k=60`, `filters` schema allowlist.
- **Phân bổ thời gian:** 20 phút đọc, 50 phút code, 25 phút tests, 15 phút ghi chú (110 phút).
- **Lý thuyết:** RRF dùng rank nên không đòi scale score; filter là constraint trước/sau retrieval cần nhất quán.
- **Tài liệu:** Qdrant Hybrid Queries và Filtering trong [RESOURCES.md](./RESOURCES.md).
- **Thực hành:** Fuse result list theo chunk_id, rồi load metadata đầy đủ.
- **Tích hợp project:** Search chỉ cho filter `category`, `document_id`, `version`; từ chối arbitrary payload key.
- **File tạo/sửa:** `app/rag/hybrid.py`, `app/rag/retrieval.py`, `tests/unit/test_hybrid.py`.
- **Lệnh chạy:** `uv run pytest tests/unit/test_hybrid.py -q`.
- **Kết quả mong đợi:** Chunk xuất hiện trong cả hai list có rank fusion tốt hơn; filter sai trả validation error.
- **Cách kiểm tra:** Fixture 2 list cố định, assert thứ tự RRF.
- **Definition of Done:** Cấu hình fusion được trả trong response/debug nội bộ để tái lập evaluation.
- **Commit message:** `feat(rag): fuse dense and lexical results with rrf`
- **Tự kiểm tra:** RRF giải quyết vấn đề gì? Filter metadata có thể gây false negative thế nào?

### Ngày 13 - Search API, observability và integration test

- **Mục tiêu:** Expose retrieval bằng HTTP contract có mode/top-k bounded.
- **Kết quả cần đạt:** `/api/v1/rag/search` validates `k` 1–10, logs mode/latency/count và không trả raw vector.
- **Phân bổ thời gian:** 15 phút thiết kế, 45 phút route, 40 phút integration test, 15 phút ghi chú (115 phút).
- **Lý thuyết:** Retrieval result là evidence, chưa là câu trả lời LLM.
- **Tài liệu:** Qdrant Search trong [RESOURCES.md](./RESOURCES.md), Tuần 2.
- **Thực hành:** Dependency inject retriever fake trong test client.
- **Tích hợp project:** Reuse error contract, request ID và timeout policy đã có từ Month-01/03.
- **File tạo/sửa:** `app/api/routes/rag.py`, `tests/integration/test_rag_search.py`, `app/core/logging.py`.
- **Lệnh chạy:** `uv run pytest tests/integration/test_rag_search.py -q`.
- **Kết quả mong đợi:** Dense/BM25/hybrid cho contract cùng shape; `k=50` nhận 422.
- **Cách kiểm tra:** Assert source_path/section/score có mặt và text được truncate theo schema.
- **Definition of Done:** Search API không gọi LLM và không có side effect.
- **Commit message:** `feat(rag): expose bounded retrieval search endpoint`
- **Tự kiểm tra:** Vì sao search endpoint không nên tự trả lời? Log nào giúp debug mà không lộ query?

### Ngày 14 - Milestone: so sánh retrieval thủ công

- **Mục tiêu:** Quan sát ba mode bằng 5 query đã định trước, chuẩn bị golden set tuần 4.
- **Kết quả cần đạt:** Bảng `docs/rag-retrieval-baseline.md` ghi query, expected source và top-3 của dense/BM25/hybrid.
- **Phân bổ thời gian:** 20 phút chọn query, 35 phút chạy search, 35 phút ghi bảng, 20 phút test/lint, 10 phút ghi chú (120 phút).
- **Lý thuyết:** Manual inspection không thay evaluation nhưng phát hiện lỗi index/config sớm.
- **Tài liệu:** Xem lại Qdrant Search/Hybrid trong [RESOURCES.md](./RESOURCES.md).
- **Thực hành:** Ingest corpus dev, chạy command từng mode; không chỉnh query để làm đẹp kết quả.
- **Tích hợp project:** Ghi config corpus/chunk/model cho baseline.
- **File tạo/sửa:** `docs/rag-retrieval-baseline.md`, `tests/integration/test_rag_search.py`.
- **Lệnh chạy:** `uv run pytest`; `uv run ruff check .`; `docker compose up -d qdrant`.
- **Kết quả mong đợi:** Có ít nhất một case BM25 thắng và một case dense/hybrid thắng hoặc ghi rõ corpus chưa đủ đa dạng.
- **Cách kiểm tra:** Bảng có link source/chunk ID để tái chạy.
- **Definition of Done:** Pipeline retrieve chạy local, ba mode được mô tả trung thực, không claim metric chưa đo.
- **Commit message:** `docs(rag): record dense bm25 and hybrid retrieval baseline`
- **Tự kiểm tra:** Case nào hybrid không cải thiện? Baseline này sẽ khóa yếu tố nào cho tuần 4?

## Milestone cuối tuần

Corpus đã index vào Qdrant và `/rag/search` trả evidence theo dense, BM25 hoặc hybrid có filter/score/metadata.

## Review checklist

- [ ] Qdrant chỉ chạy local, config và timeout rõ ràng.
- [ ] BM25 là baseline độc lập; hybrid có fusion document hóa được.
- [ ] `k` và filter được validate; không trả vector/raw secret.
- [ ] Có integration test và bảng quan sát 5 query.

## Definition of Done

Người học có retrieval interface nhất quán và baseline đủ để tuần 3 thêm answer generation, không đổi score theo cảm tính.

## Lỗi thường gặp

- Tạo collection mỗi request hoặc dùng dimension khác embedding.
- Cộng cosine score với BM25 score trực tiếp.
- Đánh giá search bằng câu trả lời LLM khi chưa có citation.

## Tài liệu tham khảo chính thức

Xem nhóm Tuần 2 trong [RESOURCES.md](./RESOURCES.md).

## Tùy chọn nếu còn thời gian

Thử Qdrant native hybrid prefetch sau khi RRF local đã có unit test; không thay baseline giữa tuần.
