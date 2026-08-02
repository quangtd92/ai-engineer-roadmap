# Tháng 04 — Tuần 03: Query rewriting, reranking, citation và safety

## Mục tiêu tuần

Chuyển kết quả hybrid search của Tuần 02 thành ngữ cảnh đáng tin cậy cho LLM: rewrite query có thể quan sát, rerank có giới hạn, citation lấy từ metadata thật, và từ chối khi bằng chứng không đủ. Tài liệu được xem là **dữ liệu không tin cậy**, không phải chỉ dẫn cho hệ thống.

## Kiến thức cần đạt

- Query rewrite là truy vấn phụ trợ có thể tắt/bật; không được thay câu hỏi người dùng hoặc đưa instruction vào prompt hệ thống.
- Reranker đánh lại thứ hạng top-N; nó không tạo nguồn mới và không thay thế evaluation.
- Citation phải tham chiếu `chunk_id`/`document_id` đã retrieve. Refusal là một kết quả đúng khi evidence thiếu.

## Tính năng project sẽ bổ sung

`src/ai_assistant_platform/rag/query_rewrite.py`, `reranker.py`, `context.py`, `citations.py`, `safety.py` và `answer_service.py`; endpoint `POST /api/v1/rag/answer` trả answer có citation hoặc trạng thái `insufficient_evidence`.

## Kế hoạch từng ngày

### Ngày 15 — Đặt contract retrieval-to-answer

- **Mục tiêu cụ thể:** Khóa kiểu dữ liệu trao đổi giữa hybrid retriever, reranker và answer service.
- **Kết quả cần đạt:** Có `RetrievedChunk`, `Citation`, `RagAnswerResponse` với `status`, `answer`, `citations`, `retrieval_config` và `request_id`.
- **Phân bổ thời gian:** 15 phút ôn output Tuần 02, 25 phút đọc, 45 phút code schema, 20 phút unit test, 10 phút ghi chú (115 phút).
- **Lý thuyết cần học:** Contract tách score nội bộ khỏi response công khai; provenance phải đi theo chunk trong mọi bước.
- **Tài liệu cần đọc:** Qdrant [Payload](https://qdrant.tech/documentation/concepts/payload/) — payload và filter metadata.
- **Bài thực hành:** Viết mapper từ search hit sang `RetrievedChunk`; cấm tạo citation từ URL/chuỗi do model trả về.
- **Tích hợp project:** Đặt schema ở `src/ai_assistant_platform/rag/schemas.py` để API và service dùng cùng contract.
- **File tạo/sửa:** `src/ai_assistant_platform/rag/schemas.py`, `src/ai_assistant_platform/rag/retrieval.py`, `tests/unit/test_rag_answer_schemas.py`.
- **Lệnh chạy:** `uv run pytest tests/unit/test_rag_answer_schemas.py -q`.
- **Kết quả mong đợi:** Schema từ chối citation thiếu `chunk_id` hoặc `document_id`.
- **Cách kiểm tra:** Deserialize fixture dense/BM25/hybrid và assert metadata cần citation vẫn còn.
- **Definition of Done:** Không response nào tin score/model-generated URL là nguồn chứng cứ.
- **Commit message gợi ý:** `feat(rag): define retrieval to answer provenance contract`
- **Câu hỏi tự kiểm tra:** Vì sao citation không chỉ là một URL? Score retrieval có nên trả thẳng cho người dùng không?

### Ngày 16 — Query rewrite có boundary

- **Mục tiêu cụ thể:** Thêm rewrite đơn giản cho query mơ hồ, có fallback nguyên văn và log an toàn.
- **Kết quả cần đạt:** `rewrite_query()` trả `original_query`, `search_query`, `rewritten=False/True`; input quá dài hoặc có control text dùng nguyên query sau validation.
- **Phân bổ thời gian:** 20 phút lý thuyết, 45 phút code/fake LLM, 30 phút test, 15 phút ghi chú (110 phút).
- **Lý thuyết cần học:** Rewrite nhằm tăng recall, không được trả lời câu hỏi hay thay đổi permission/filter của request.
- **Tài liệu cần đọc:** OpenAI [Safety best practices](https://platform.openai.com/docs/guides/safety-best-practices) — untrusted input và prompt injection.
- **Bài thực hành:** Dùng interface LLM Month-03/fake client; prompt yêu cầu chỉ trả một search query, Pydantic validate rồi fallback nếu lỗi.
- **Tích hợp project:** Ghi `rewrite_applied` và hash query vào telemetry, không log nguyên query nếu chính sách project coi đó là nhạy cảm.
- **File tạo/sửa:** `src/ai_assistant_platform/rag/query_rewrite.py`, `src/ai_assistant_platform/rag/schemas.py`, `tests/unit/test_query_rewrite.py`.
- **Lệnh chạy:** `uv run pytest tests/unit/test_query_rewrite.py -q`.
- **Kết quả mong đợi:** Fixture malformed output và timeout không làm endpoint lỗi; retrieval dùng original query.
- **Cách kiểm tra:** Assert fake client không được gọi khi `rewrite_enabled=False` và filter metadata không đổi sau rewrite.
- **Definition of Done:** Rewrite có timeout ngắn, fallback xác định và không sinh câu trả lời.
- **Commit message gợi ý:** `feat(rag): add bounded query rewrite with fallback`
- **Câu hỏi tự kiểm tra:** Rewrite cải thiện recall hay faithfulness? Vì sao không để rewrite chọn collection?

### Ngày 17 — Reranker top-N xuống context candidates

- **Mục tiêu cụ thể:** Rerank một tập candidate hữu hạn sau hybrid retrieval.
- **Kết quả cần đạt:** `Reranker.rank(query, candidates)` nhận tối đa 10 chunk và trả tối đa 4 chunk, giữ nguyên provenance và thứ tự mới.
- **Phân bổ thời gian:** 20 phút đọc, 45 phút code adapter/fake scorer, 30 phút unit test, 15 phút ghi chú (110 phút).
- **Lý thuyết cần học:** Bi-encoder tìm nhanh; cross-encoder/LLM reranker chậm hơn nhưng xét query-chunk cùng lúc. Chỉ dùng ở tập nhỏ.
- **Tài liệu cần đọc:** Qdrant [Search](https://qdrant.tech/documentation/concepts/search/) — score/top-k; ghi chú reranker là bước ứng dụng sau retrieval.
- **Bài thực hành:** Bắt đầu deterministic lexical scorer cho test; tách adapter để model reranker thật là tùy chọn sau này.
- **Tích hợp project:** `HybridRetriever` trả top-10, `AnswerService` gọi reranker trước context assembly.
- **File tạo/sửa:** `src/ai_assistant_platform/rag/reranker.py`, `src/ai_assistant_platform/rag/answer_service.py`, `tests/unit/test_reranker.py`.
- **Lệnh chạy:** `uv run pytest tests/unit/test_reranker.py -q`.
- **Kết quả mong đợi:** Candidate relevance cao đi lên; duplicate `chunk_id` chỉ xuất hiện một lần.
- **Cách kiểm tra:** Test tie-break theo `chunk_id` để output reproducible, đồng thời assert reranker không nhận hơn 10 candidate.
- **Definition of Done:** Không fine-tune/download model lớn và không bỏ metadata trong quá trình rerank.
- **Commit message gợi ý:** `feat(rag): rerank bounded hybrid retrieval candidates`
- **Câu hỏi tự kiểm tra:** Vì sao không rerank toàn bộ collection? Reranking tác động metric nào trước tiên?

### Ngày 18 — Context budget và chống lặp evidence

- **Mục tiêu cụ thể:** Tạo context từ reranked chunk trong một budget có thể đo.
- **Kết quả cần đạt:** `build_context()` chọn tối đa 4 chunk, có tổng `max_chars`, đánh số `[S1]...[S4]` và loại duplicate document-section.
- **Phân bổ thời gian:** 15 phút ôn, 25 phút lý thuyết, 45 phút code, 25 phút test, 10 phút ghi chú (120 phút).
- **Lý thuyết cần học:** Context dài hơn không luôn tốt: chi phí, latency và distractor tăng; context compression ở đây là selection xác định, không phải tóm tắt mất nguồn.
- **Tài liệu cần đọc:** OpenAI [Embeddings guide](https://platform.openai.com/docs/guides/embeddings) — giới hạn input và batching (chỉ phần khái niệm).
- **Bài thực hành:** Chọn chunk theo rank, cắt tại ranh giới câu khi có thể, kèm map label → chunk metadata.
- **Tích hợp project:** `AnswerService` gửi context builder output vào prompt Month-03 và ghi `context_chars`, `context_chunks`.
- **File tạo/sửa:** `src/ai_assistant_platform/rag/context.py`, `src/ai_assistant_platform/rag/answer_service.py`, `tests/unit/test_context.py`.
- **Lệnh chạy:** `uv run pytest tests/unit/test_context.py -q`.
- **Kết quả mong đợi:** Không vượt budget; citation map vẫn tham chiếu toàn bộ chunk nguồn khi text bị cắt.
- **Cách kiểm tra:** Fixture 5 chunk dài xác minh chunk thứ năm và duplicate section bị bỏ theo policy rõ ràng.
- **Definition of Done:** Budget là config, không hard-code trong prompt, và log chỉ ghi count/length.
- **Commit message gợi ý:** `feat(rag): assemble bounded cited retrieval context`
- **Câu hỏi tự kiểm tra:** Context compression khác reranking thế nào? Cắt text có rủi ro gì cho citation?

### Ngày 19 — Answer grounded và citation xác thực

- **Mục tiêu cụ thể:** Sinh câu trả lời cấu trúc từ context và chuyển citation label thành metadata thật.
- **Kết quả cần đạt:** Structured `GroundedAnswer` gồm answer, `used_source_labels`, confidence policy; `CitationBuilder` chỉ map label đã có trong context.
- **Phân bổ thời gian:** 20 phút đọc contract Structured Output, 50 phút code, 30 phút unit test, 10 phút ghi chú (110 phút).
- **Lý thuyết cần học:** Model có thể nói có nguồn nhưng trích sai; validation hậu xử lý là boundary cuối cùng.
- **Tài liệu cần đọc:** Pydantic [Models](https://docs.pydantic.dev/latest/concepts/models/) — validation và errors.
- **Bài thực hành:** Prompt yêu cầu trả JSON/schema Month-03, citation bằng `[S#]`; reject label lạ và fallback sang `insufficient_evidence` nếu không có citation hợp lệ.
- **Tích hợp project:** Tái sử dụng LLM adapter và usage/latency logging của Month-03, không tạo client mới trong route.
- **File tạo/sửa:** `src/ai_assistant_platform/rag/answer_service.py`, `src/ai_assistant_platform/rag/citations.py`, `tests/unit/test_citations.py`.
- **Lệnh chạy:** `uv run pytest tests/unit/test_citations.py -q`.
- **Kết quả mong đợi:** `[S9]` hoặc URL model tự bịa không xuất hiện trong response public.
- **Cách kiểm tra:** Dùng fake LLM trả label hợp lệ, label lạ và JSON sai; assert status mỗi case.
- **Definition of Done:** Citation response có title/source path/section từ metadata, không từ text model.
- **Commit message gợi ý:** `feat(rag): validate grounded answer citations against retrieved chunks`
- **Câu hỏi tự kiểm tra:** Vì sao Pydantic pass vẫn chưa chứng minh citation đúng? Khi nào nên từ chối thay vì sửa citation?

### Ngày 20 — Refusal khi evidence không đủ

- **Mục tiêu cụ thể:** Định nghĩa policy trả lời thiếu chứng cứ trước khi expose endpoint.
- **Kết quả cần đạt:** `insufficient_evidence` khi zero hit, rerank score dưới threshold cấu hình hoặc citation bị invalid; response giải thích cách người dùng cung cấp tài liệu liên quan.
- **Phân bổ thời gian:** 20 phút lý thuyết, 45 phút policy/code, 30 phút tests, 15 phút ghi chú (110 phút).
- **Lý thuyết cần học:** Retrieval score không phải confidence tuyệt đối; threshold là baseline phải được điều chỉnh bằng golden set tuần 4.
- **Tài liệu cần đọc:** OpenAI [Safety best practices](https://platform.openai.com/docs/guides/safety-best-practices) — safe completion và uncertainty.
- **Bài thực hành:** Tạo `EvidencePolicy`; test zero/low/valid evidence, không dùng LLM judge để quyết định safety cơ bản.
- **Tích hợp project:** `POST /rag/answer` sẽ dùng status phân biệt technical error với thiếu knowledge base.
- **File tạo/sửa:** `src/ai_assistant_platform/rag/safety.py`, `src/ai_assistant_platform/rag/answer_service.py`, `tests/unit/test_evidence_policy.py`.
- **Lệnh chạy:** `uv run pytest tests/unit/test_evidence_policy.py -q`.
- **Kết quả mong đợi:** Query ngoài corpus không nhận câu trả lời tự tin hay citation rỗng.
- **Cách kiểm tra:** Assert response 200 với `status="insufficient_evidence"`, còn Qdrant timeout thành lỗi service được phân loại.
- **Definition of Done:** Policy và threshold được ghi rõ, chưa tự tuyên bố score là xác suất thật.
- **Commit message gợi ý:** `feat(rag): refuse answers without sufficient retrieved evidence`
- **Câu hỏi tự kiểm tra:** Thiếu evidence khác upstream error thế nào? Threshold sẽ được kiểm chứng bằng dữ liệu nào?

### Ngày 21 — Milestone: Prompt injection trong tài liệu và API answer

- **Mục tiêu cụ thể:** Kết nối pipeline answer và chứng minh document instruction không chiếm quyền điều khiển.
- **Kết quả cần đạt:** `POST /api/v1/rag/answer` có response model; fixture chunk “ignore previous instructions” chỉ được coi là quoted data và bị safety policy đánh dấu/loại.
- **Phân bổ thời gian:** 15 phút ôn, 25 phút đọc, 50 phút route/service integration, 20 phút integration test, 10 phút smoke test (120 phút).
- **Lý thuyết cần học:** Boundary: system/developer policy > user query > retrieved content. Filter có thể giảm rủi ro nhưng không là chứng minh an toàn hoàn hảo.
- **Tài liệu cần đọc:** OpenAI [Safety best practices](https://platform.openai.com/docs/guides/safety-best-practices) — prompt injection; FastAPI response model (Month-01 recap).
- **Bài thực hành:** Gắn untrusted-content delimiters vào prompt, keyword policy tối thiểu để flag text nguy hiểm, và không cho document thay query/filter/tool policy.
- **Tích hợp project:** Route inject `AnswerService`; log outcome/retrieval config, không log context đầy đủ.
- **File tạo/sửa:** `src/ai_assistant_platform/api/routes/rag.py`, `src/ai_assistant_platform/rag/safety.py`, `src/ai_assistant_platform/rag/answer_service.py`, `tests/integration/test_rag_answer.py`.
- **Lệnh chạy:** `uv run pytest tests/integration/test_rag_answer.py -q`.
- **Kết quả mong đợi:** Valid fixture trả citation; injection fixture không dẫn tới disclosure, tool call hoặc thay system instruction.
- **Cách kiểm tra:** Assert prompt passed to fake LLM có delimiters, response không chứa secret fixture và `safety_flags` được internal-only.
- **Definition of Done:** Endpoint không nhận arbitrary URL/file, có timeout, và test cả grounded/refusal/injection path.
- **Commit message gợi ý:** `feat(rag): expose grounded answer endpoint with document injection defense`
- **Câu hỏi tự kiểm tra:** Vì sao delimiters không đủ một mình? Tại sao document không được gọi tool?

## Milestone cuối tuần

Pipeline `rewrite → hybrid retrieve → rerank → bounded context → structured answer` trả citation xác thực hoặc `insufficient_evidence`; injection trong document không thể thay đổi policy hay gọi capability.

## Review checklist

- [ ] Rewrite có timeout/fallback và không đổi collection/filter.
- [ ] Reranker chỉ nhận top-N, giữ provenance và có output deterministic trong test.
- [ ] Context có budget, source labels và không duplicate evidence.
- [ ] Citation chỉ lấy từ chunk đã retrieve/rerank.
- [ ] Có test zero evidence, malformed output và prompt injection document.
- [ ] Không thêm agent, tool side effect hoặc framework retrieval thay thế.

## Definition of Done tuần

`POST /api/v1/rag/answer` có integration test cho grounded answer, refusal và injection fixture. Toàn bộ response trace được từ citation đến chunk/version; latency/config đủ cho evaluation Tuần 04.

## Lỗi thường gặp

- Để rewrite thay đổi câu hỏi người dùng hoặc metadata filter.
- Coi rerank score là xác suất sự thật.
- Chép citation URL từ LLM thay vì metadata.
- Để retrieved text viết lại system instruction hoặc gọi tool.

## Tài liệu tham khảo chính thức

Xem nhóm Tuần 03 trong [RESOURCES.md](./RESOURCES.md), cùng Pydantic/OpenAI links nêu tại từng ngày.

## Tùy chọn nếu còn thời gian

Thử multi-query retrieval bằng hai rewrite có dedupe và budget chung, nhưng chỉ sau khi benchmark single-query baseline; không đưa vào evaluation gate bắt buộc.
