# Tháng 4 - Tuần 1: Ingestion, chunking và metadata

## Mục tiêu tuần

Tạo pipeline biến Markdown/TXT trong corpus local thành chunk có thể truy vết, versioned và an toàn để đưa vào Qdrant tuần sau.

## Kiến thức cần đạt

- Phân biệt document, chunk, metadata, fingerprint và vector (chưa tạo embedding tuần này).
- Chọn chunk theo heading + số ký tự, không cắt tùy tiện giữa câu.
- Chỉ ingest file trong thư mục allowlist; không tin instruction nằm trong nội dung tài liệu.

## Tính năng project sẽ bổ sung

`src/ai_assistant_platform/rag/ingestion.py`, schema chunk và `POST /api/v1/rag/ingest` ở chế độ dry-run, trả số chunk/duplicate trước khi ghi database.

## Kế hoạch từng ngày

### Ngày 1 - Xác định corpus và hợp đồng ingestion

- **Mục tiêu:** Chọn corpus demo nhỏ và định nghĩa input/output của ingestion.
- **Kết quả cần đạt:** Ba Markdown/TXT công khai/tự viết trong `data/knowledge_base/` và `IngestRequest`, `IngestSummary` Pydantic.
- **Phân bổ thời gian:** 15 phút ôn Month-03, 20 phút lý thuyết, 45 phút tạo corpus/schema, 20 phút kiểm tra, 10 phút ghi chú (110 phút).
- **Lý thuyết:** Document gốc khác chunk; corpus demo không chứa PII, secret hoặc license mơ hồ.
- **Tài liệu:** Python `pathlib` trong [RESOURCES.md](./RESOURCES.md), Tuần 1.
- **Thực hành:** Viết README corpus nêu nguồn, `source_id`, `title`, `category`.
- **Tích hợp project:** Thêm `src/ai_assistant_platform/rag/schemas.py` và route placeholder chỉ validate path tương đối.
- **File tạo/sửa:** `data/knowledge_base/*.md`, `data/knowledge_base/README.md`, `src/ai_assistant_platform/rag/schemas.py`, `src/ai_assistant_platform/api/routes/rag.py`.
- **Lệnh chạy:** `uv run pytest tests/unit/test_rag_schemas.py -q`.
- **Kết quả mong đợi:** Path tuyệt đối hoặc `..` bị schema từ chối.
- **Cách kiểm tra:** Gửi `{"paths":["../../.env"]}` qua test client và nhận 422.
- **Definition of Done:** Corpus có ít nhất ba tài liệu và mọi path request đều tương đối với allowlist.
- **Commit message:** `feat(rag): define local corpus and ingest schemas`
- **Tự kiểm tra:** Vì sao user không được gửi URL để server tự tải? Metadata nào cần có trước khi chunk?

### Ngày 2 - Parse và chuẩn hóa Markdown/TXT

- **Mục tiêu:** Đọc UTF-8 ổn định và giữ heading làm ngữ cảnh.
- **Kết quả cần đạt:** `ParsedDocument` có text sạch, heading hiện tại và lỗi nêu rõ file.
- **Phân bổ thời gian:** 15 phút đọc, 25 phút lý thuyết, 45 phút code, 20 phút test, 10 phút ghi chú (115 phút).
- **Lý thuyết:** Normalize line ending/whitespace nhưng không làm mất code block hay tiêu đề.
- **Tài liệu:** Python `pathlib` và encoding trong [RESOURCES.md](./RESOURCES.md), Tuần 1.
- **Thực hành:** Viết `parse_document(path)` cho `.md`, `.txt`; từ chối extension khác.
- **Tích hợp project:** Ingestion route gọi parser ở dry-run và trả danh sách lỗi theo file.
- **File tạo/sửa:** `src/ai_assistant_platform/rag/parser.py`, `tests/unit/test_rag_parser.py`, `src/ai_assistant_platform/api/routes/rag.py`.
- **Lệnh chạy:** `uv run pytest tests/unit/test_rag_parser.py -q`.
- **Kết quả mong đợi:** File UTF-8 được parse; `.pdf` nhận lỗi có chủ đích.
- **Cách kiểm tra:** Thêm fixture có CRLF và heading; assert heading/text sau normalize.
- **Definition of Done:** Parser không đọc ngoài `data/knowledge_base` và không im lặng bỏ qua lỗi decode.
- **Commit message:** `feat(rag): parse allowlisted markdown and text documents`
- **Tự kiểm tra:** Heading giúp retrieval thế nào? Vì sao PDF không nên thêm vội ở ngày này?

### Ngày 3 - Chunk theo cấu trúc và overlap có chủ đích

- **Mục tiêu:** Chia document thành chunk đọc được mà không vượt context budget.
- **Kết quả cần đạt:** Chunk 600 ký tự, overlap 80 ký tự, ưu tiên ranh giới đoạn/heading.
- **Phân bổ thời gian:** 20 phút lý thuyết, 50 phút implementation, 25 phút test biên, 15 phút ghi chú (110 phút).
- **Lý thuyết:** Trade-off chunk size, overlap, recall và context noise; các số này là baseline để evaluation tuần 4.
- **Tài liệu:** Qdrant Points trong [RESOURCES.md](./RESOURCES.md), Tuần 1 (liên hệ point/chunk).
- **Thực hành:** Viết `chunk_document(parsed, max_chars=600, overlap=80)`.
- **Tích hợp project:** `IngestSummary` trả `chunk_count` và cấu hình chunking.
- **File tạo/sửa:** `src/ai_assistant_platform/rag/chunking.py`, `tests/unit/test_chunking.py`, `src/ai_assistant_platform/rag/schemas.py`.
- **Lệnh chạy:** `uv run pytest tests/unit/test_chunking.py -q`.
- **Kết quả mong đợi:** Không chunk nào rỗng; chunk dài không quá giới hạn trừ một token/đoạn đơn lẻ được ghi nhận.
- **Cách kiểm tra:** Fixture có heading dài và paragraph dài; assert overlap chỉ xuất hiện ở split bắt buộc.
- **Definition of Done:** Test chứng minh content cuối chunk trước xuất hiện có kiểm soát ở chunk sau.
- **Commit message:** `feat(rag): add structure-aware text chunking`
- **Tự kiểm tra:** Chunk nhỏ quá gây hại metric nào? Overlap có phải lúc nào cũng tăng chất lượng?

### Ngày 4 - Metadata, ID ổn định và document version

- **Mục tiêu:** Gắn provenance đủ để citation và re-ingest an toàn.
- **Kết quả cần đạt:** Mỗi chunk có `chunk_id`, `document_id`, `version`, `source_path`, `title`, `section`, `chunk_index`.
- **Phân bổ thời gian:** 20 phút đọc, 45 phút code, 25 phút unit test, 20 phút tích hợp route (110 phút).
- **Lý thuyết:** ID ổn định phục vụ upsert; version là thuộc tính dữ liệu, không phải timestamp ngẫu nhiên.
- **Tài liệu:** Qdrant Payload trong [RESOURCES.md](./RESOURCES.md), Tuần 1.
- **Thực hành:** Tạo UUID5 từ source path + version + chunk index.
- **Tích hợp project:** Dry-run trả sample metadata, không trả toàn bộ text lớn.
- **File tạo/sửa:** `src/ai_assistant_platform/rag/metadata.py`, `src/ai_assistant_platform/rag/schemas.py`, `tests/unit/test_rag_metadata.py`.
- **Lệnh chạy:** `uv run pytest tests/unit/test_rag_metadata.py -q`.
- **Kết quả mong đợi:** Chạy cùng input hai lần cho cùng ID; đổi version cho ID khác.
- **Cách kiểm tra:** So sánh ID của ba lần gọi trong unit test.
- **Definition of Done:** Không dùng filename đơn lẻ làm document ID vì có thể trùng khi mở rộng corpus.
- **Commit message:** `feat(rag): attach versioned chunk provenance metadata`
- **Tự kiểm tra:** Citation cần metadata nào? Tại sao timestamp không thích hợp làm deterministic ID?

### Ngày 5 - Fingerprint và deduplication

- **Mục tiêu:** Nhận biết chunk có nội dung đã ingest, kể cả đổi whitespace.
- **Kết quả cần đạt:** SHA-256 của normalized text và report `new_chunks`/`duplicate_chunks`.
- **Phân bổ thời gian:** 15 phút lý thuyết, 50 phút code, 30 phút test, 15 phút ghi chú (110 phút).
- **Lý thuyết:** Fingerprint không thay semantic duplicate; baseline chỉ giải quyết duplicate byte-normalized.
- **Tài liệu:** Python `hashlib` trong [RESOURCES.md](./RESOURCES.md), Tuần 1.
- **Thực hành:** Thêm `content_sha256`, repository in-memory để test quyết định skip.
- **Tích hợp project:** Dry-run báo chunk trùng trước khi Qdrant được thêm ở tuần 2.
- **File tạo/sửa:** `src/ai_assistant_platform/rag/fingerprints.py`, `src/ai_assistant_platform/rag/ingestion.py`, `tests/unit/test_fingerprints.py`.
- **Lệnh chạy:** `uv run pytest tests/unit/test_fingerprints.py -q`.
- **Kết quả mong đợi:** “A  B” và “A B” có cùng hash sau normalize; text khác có hash khác.
- **Cách kiểm tra:** Assert count duplicate khi ingest fixture lặp.
- **Definition of Done:** Hash không được log cùng nội dung tài liệu nhạy cảm.
- **Commit message:** `feat(rag): detect duplicate chunks by normalized fingerprint`
- **Tự kiểm tra:** Fingerprint bỏ sót dạng duplicate nào? Vì sao không dùng Python `hash()`?

### Ngày 6 - Milestone: endpoint dry-run và integration test

- **Mục tiêu:** Nối parse → chunk → metadata → dedupe qua HTTP contract.
- **Kết quả cần đạt:** `POST /api/v1/rag/ingest?dry_run=true` trả summary xác định được.
- **Phân bổ thời gian:** 15 phút ôn, 30 phút route/dependency, 50 phút integration test, 20 phút sửa, 5 phút ghi chú (120 phút).
- **Lý thuyết:** Integration test kiểm tra wiring; unit test vẫn là nơi cover split edge case.
- **Tài liệu:** FastAPI request body (đã học Month-01) và Qdrant Points trong [RESOURCES.md](./RESOURCES.md).
- **Thực hành:** Inject corpus root test, không dùng corpus thật trong test.
- **Tích hợp project:** Đăng ký rag router trong `src/ai_assistant_platform/main.py`, log count/latency thay vì raw document.
- **File tạo/sửa:** `src/ai_assistant_platform/api/routes/rag.py`, `src/ai_assistant_platform/main.py`, `tests/integration/test_rag_ingest.py`.
- **Lệnh chạy:** `uv run pytest tests/integration/test_rag_ingest.py -q`.
- **Kết quả mong đợi:** 200 có count; request extension không cho phép trả 422/400 rõ ràng.
- **Cách kiểm tra:** Chạy test hai lần, response summary giữ nguyên.
- **Definition of Done:** Endpoint không ghi data, không cần Qdrant và không leak filesystem path tuyệt đối.
- **Commit message:** `feat(rag): expose validated ingestion dry run endpoint`
- **Tự kiểm tra:** Vì sao dry-run nên có trước write path? Unit và integration test đang chứng minh điều gì khác nhau?

### Ngày 7 - Review, quality gate và handoff Qdrant

- **Mục tiêu:** Khóa baseline ingestion trước khi thêm vector store.
- **Kết quả cần đạt:** Test/lint pass, ADR ngắn ghi chunk size/version policy và backlog parser PDF là optional.
- **Phân bổ thời gian:** 25 phút review, 35 phút refactor, 20 phút test/lint, 20 phút ADR hoặc nghỉ bù (100 phút).
- **Lý thuyết:** Reproducibility: cùng corpus + config phải sinh cùng point ID/fingerprint.
- **Tài liệu:** Xem lại Tuần 1 trong [RESOURCES.md](./RESOURCES.md).
- **Thực hành:** Viết `docs/adr/0001-rag-ingestion-baseline.md`; xóa code chết, không thêm feature.
- **Tích hợp project:** Chuẩn bị interface `ChunkStore.upsert()` để tuần 2 thay in-memory bằng Qdrant.
- **File tạo/sửa:** `docs/adr/0001-rag-ingestion-baseline.md`, `src/ai_assistant_platform/rag/ingestion.py`, tests liên quan.
- **Lệnh chạy:** `uv run ruff check .`; `uv run pytest tests/unit tests/integration -q`.
- **Kết quả mong đợi:** Hai lệnh pass, ADR nêu rõ version và dedupe scope.
- **Cách kiểm tra:** Review diff; xác nhận chưa import Qdrant client hay embedding SDK.
- **Definition of Done:** Có một corpus chunked reproducible và quality gate xanh.
- **Commit message:** `docs(rag): record ingestion and chunking baseline`
- **Tự kiểm tra:** Quyết định nào tuần này là baseline phải giữ cố định khi đánh giá? Điều gì được hoãn sang tuần 2?

## Milestone cuối tuần

Dry-run ingestion an toàn sinh chunk có provenance, ID/version deterministic và phát hiện duplicate cho corpus local.

## Review checklist

- [ ] 7 ngày có test hoặc verification riêng.
- [ ] Không parse URL, path traversal, PDF/OCR hay database trước khi giới thiệu.
- [ ] Corpus không chứa secret/PII; log không in raw chunk.
- [ ] `uv run pytest` và `uv run ruff check .` pass.

## Definition of Done

Pipeline dry-run cho cùng corpus/config tạo kết quả lặp lại được, sẵn sàng upsert Qdrant ở tuần 2.

## Lỗi thường gặp

- Chia theo số ký tự mà bỏ hoàn toàn heading/paragraph.
- Coi semantic duplicate và hash duplicate là một.
- Cho API đọc bất kỳ path nào từ request.

## Tài liệu tham khảo chính thức

Xem nhóm Tuần 1 trong [RESOURCES.md](./RESOURCES.md).

## Tùy chọn nếu còn thời gian

Thêm parser PDF ở branch riêng sau khi viết test giới hạn dung lượng; không đưa vào milestone bắt buộc.
