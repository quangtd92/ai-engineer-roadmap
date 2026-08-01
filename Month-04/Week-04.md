# Tháng 04 — Tuần 04: RAG evaluation, regression và bàn giao agent

## Mục tiêu tuần

Đánh giá RAG như một hệ thống có dữ liệu và tiêu chí, không phải demo. Tuần này tạo golden set, chạy baseline dense so với hybrid+rerank, kết hợp assertion xác định với RAGAS **hoặc** DeepEval, rồi viết error analysis và contract để Month-05 dùng RAG như capability bị giới hạn.

## Kiến thức cần đạt

- Tách unit/integration test khỏi retrieval evaluation và LLM-as-judge evaluation.
- Metric không thay thế review lỗi: context precision/recall, faithfulness, answer relevancy, latency và cost/usage trả lời các câu hỏi khác nhau.
- Một gate chỉ có giá trị khi dataset, config, threshold và failure report được versioned.

## Tính năng project sẽ bổ sung

`evals/rag/golden_questions.jsonl`, runner `evals/rag/run_rag_eval.py`, report Markdown/JSON, test regression cho retrieval contract và `docs/month-05-handoff.md`.

## Kế hoạch từng ngày

### Ngày 22 — Phân loại câu hỏi và thiết kế golden set

- **Mục tiêu cụ thể:** Thiết kế dataset nhỏ, cân bằng và có ground truth provenance.
- **Kết quả cần đạt:** Schema JSONL có `id`, `question`, `expected_answer`, `expected_chunk_ids`, `category`, `difficulty`, `notes`; kế hoạch 10–15 case.
- **Phân bổ thời gian:** 20 phút đọc, 45 phút viết dataset, 25 phút schema validation, 15 phút review (105 phút).
- **Lý thuyết cần học:** Golden question đại diện cho use case, không chỉ câu dễ; expected context cho phép đo retrieval riêng khỏi generation.
- **Tài liệu cần đọc:** RAGAS [Get started](https://docs.ragas.io/en/stable/getstarted/) — dataset/evaluate flow.
- **Bài thực hành:** Lấy câu hỏi từ 3–8 tài liệu corpus; thêm ít nhất hai case không có đáp án để test refusal.
- **Tích hợp project:** Dataset chỉ tham chiếu `chunk_id`/document version từ pipeline, không copy secret hoặc tài liệu có license không rõ.
- **File tạo/sửa:** `evals/rag/golden_questions.jsonl`, `evals/rag/schema.py`, `tests/unit/test_rag_eval_dataset.py`.
- **Lệnh chạy:** `uv run pytest tests/unit/test_rag_eval_dataset.py -q`.
- **Kết quả mong đợi:** Mỗi ID unique; expected chunk tồn tại trong fixture manifest; case refusal có expected context rỗng.
- **Cách kiểm tra:** Parse từng dòng JSONL và assert đủ category factual, multi-section, lexical, semantic, no-answer.
- **Definition of Done:** Dataset có source provenance do con người kiểm tra, không sinh tự động bằng chính model đang đánh giá.
- **Commit message gợi ý:** `test(rag): add versioned golden question dataset`
- **Câu hỏi tự kiểm tra:** Vì sao expected answer chưa đủ để đánh giá retrieval? No-answer case đo gì?

### Ngày 23 — Chạy retrieval baseline dense

- **Mục tiêu cụ thể:** Thu metric retrieval không có LLM judge cho dense baseline.
- **Kết quả cần đạt:** Runner ghi per-case top-k `chunk_ids`, hit@k, MRR, latency và config `dense_top_k=10`.
- **Phân bổ thời gian:** 15 phút ôn dataset, 25 phút lý thuyết, 50 phút runner, 20 phút test, 10 phút ghi chú (120 phút).
- **Lý thuyết cần học:** Hit@k trả lời “có evidence đúng trong top-k không”; MRR thưởng cho evidence đứng sớm. Hai metric không đo answer chất lượng.
- **Tài liệu cần đọc:** pytest [Parametrize](https://docs.pytest.org/en/stable/how-to/parametrize.html) — test dữ liệu-driven.
- **Bài thực hành:** Implement `run_retrieval_eval(config)` dùng fake/local corpus deterministic; lưu JSON artifact có timestamp và dataset version.
- **Tích hợp project:** Gọi retriever interface Tuần 02, không sao chép thuật toán Qdrant trong runner.
- **File tạo/sửa:** `evals/rag/run_rag_eval.py`, `evals/rag/metrics.py`, `tests/unit/test_retrieval_metrics.py`.
- **Lệnh chạy:** `uv run pytest tests/unit/test_retrieval_metrics.py -q`; `uv run python evals/rag/run_rag_eval.py --config dense`.
- **Kết quả mong đợi:** Có report dense, mỗi case có ranking/latency và aggregate hit@k/MRR.
- **Cách kiểm tra:** Case có expected chunk ở rank 1 tạo reciprocal rank 1; missing chunk tạo 0.
- **Definition of Done:** Runner exit non-zero khi dataset invalid, không silent-skip case.
- **Commit message gợi ý:** `test(rag): measure dense retrieval baseline`
- **Câu hỏi tự kiểm tra:** Hit@10 cao nhưng MRR thấp nói gì? Vì sao không dùng answer text để tính hit@k?

### Ngày 24 — So sánh hybrid và reranking

- **Mục tiêu cụ thể:** Chạy cùng dataset với cấu hình hybrid+rerank và so sánh công bằng.
- **Kết quả cần đạt:** Một config file/CLI preset khác, report delta theo hit@k, MRR, p50/p95 latency và case thắng/thua.
- **Phân bổ thời gian:** 20 phút đọc, 45 phút code/report comparison, 30 phút chạy fixtures, 15 phút ghi chú (110 phút).
- **Lý thuyết cần học:** So sánh chỉ hợp lệ khi corpus, dataset, top-k và điều kiện chạy giống nhau; hybrid có trade-off latency.
- **Tài liệu cần đọc:** Qdrant [Hybrid queries](https://qdrant.tech/documentation/concepts/hybrid-queries/) — fusion/prefetch.
- **Bài thực hành:** Gắn `--config hybrid_rerank`, lưu retrieval config đầy đủ và tính delta không làm tròn quá sớm.
- **Tích hợp project:** Dùng `RetrievalConfig` của service làm input runner để production/eval không drift.
- **File tạo/sửa:** `evals/rag/configs.py`, `evals/rag/reporting.py`, `tests/unit/test_rag_comparison.py`.
- **Lệnh chạy:** `uv run pytest tests/unit/test_rag_comparison.py -q`; `uv run python evals/rag/run_rag_eval.py --config hybrid_rerank --compare dense`.
- **Kết quả mong đợi:** Báo cáo có hai cấu hình, dataset hash và danh sách case regression; không tuyên bố hybrid luôn tốt hơn.
- **Cách kiểm tra:** Dùng fixture synthetic khiến lexical query thắng BM25 để test report ghi đúng winner/loser.
- **Definition of Done:** Có ít nhất hai cấu hình retrieval được so sánh bằng cùng metric và cùng test data.
- **Commit message gợi ý:** `test(rag): compare hybrid reranking against dense baseline`
- **Câu hỏi tự kiểm tra:** Khi nào dense thắng hybrid? Tại sao p95 quan trọng hơn chỉ average latency?

### Ngày 25 — Ghi expected behavior và regression gate

- **Mục tiêu cụ thể:** Chuyển một phần golden set thành regression test nhanh, xác định.
- **Kết quả cần đạt:** 5–8 canonical case có expectation top-k/refusal/citation; gate fail nếu hit@k dưới threshold baseline đã ghi.
- **Phân bổ thời gian:** 20 phút lý thuyết, 45 phút pytest, 30 phút threshold review, 15 phút ghi chú (110 phút).
- **Lý thuyết cần học:** Regression gate bắt lỗi thay đổi rõ ràng; không dùng LLM judge trong test bắt buộc nếu làm CI không ổn định.
- **Tài liệu cần đọc:** pytest [Parametrize](https://docs.pytest.org/en/stable/how-to/parametrize.html) — ids và fixture.
- **Bài thực hành:** Viết `tests/evaluation/test_rag_regression.py` dùng fake embedding/reranker hoặc snapshot fixture để reproducible.
- **Tích hợp project:** Đặt threshold khởi đầu thực tế (ví dụ hit@5 >= 0.70 trên small set) trong config có comment; không giả vờ universal benchmark.
- **File tạo/sửa:** `tests/evaluation/test_rag_regression.py`, `evals/rag/thresholds.py`, `docs/adr/0002-rag-evaluation-gate.md`.
- **Lệnh chạy:** `uv run pytest tests/evaluation/test_rag_regression.py -q`.
- **Kết quả mong đợi:** A known regression có thể làm test đỏ; fixture đúng pass mà không cần API key.
- **Cách kiểm tra:** Cố ý thay expected chunk trong local test (không commit) để thấy assertion fail và message chỉ ra case ID.
- **Definition of Done:** Threshold có baseline/dataset version và không dựa trên một metric generation duy nhất.
- **Commit message gợi ý:** `test(rag): add deterministic retrieval regression gate`
- **Câu hỏi tự kiểm tra:** Vì sao không gate faithfulness bằng một assert string? Threshold nên được thay đổi khi nào?

### Ngày 26 — Chọn và chạy một evaluator RAGAS hoặc DeepEval

- **Mục tiêu cụ thể:** Thêm một evaluation layer cho answer grounding, chọn đúng một framework bắt buộc.
- **Kết quả cần đạt:** Chạy **RAGAS hoặc DeepEval** trên subset 5 case, lưu faithfulness/answer relevancy (và context metric nếu tool hỗ trợ) cùng raw status/failure.
- **Phân bổ thời gian:** 25 phút đọc, 35 phút setup adapter, 35 phút chạy subset/fallback, 15 phút ghi chú (110 phút).
- **Lý thuyết cần học:** LLM-as-judge có variance/cost; metric là tín hiệu để review, không verdict duy nhất. Không chạy cả hai framework trong scope 2 giờ.
- **Tài liệu cần đọc:** RAGAS [Metrics](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/) **hoặc** DeepEval [RAG evaluation](https://deepeval.com/docs/getting-started-rag) — chọn một.
- **Bài thực hành:** Tạo adapter chuyển `RagRunRecord` sang format evaluator; đọc provider/key từ `.env` nếu cần, còn CI chỉ chạy deterministic gate.
- **Tích hợp project:** Reuse answer/context/citation thu ở Tuần 03; record model/evaluator version, latency/cost nếu có.
- **File tạo/sửa:** `evals/rag/run_llm_eval.py`, `evals/rag/evaluator_adapter.py`, `.env.example`, `docs/adr/0003-rag-evaluator-choice.md`.
- **Lệnh chạy:** `uv run python evals/rag/run_llm_eval.py --subset smoke`; `uv run pytest tests/evaluation/test_rag_regression.py -q`.
- **Kết quả mong đợi:** Có report hoặc trạng thái `skipped_missing_credentials` có chủ đích; deterministic regression vẫn pass không cần secret.
- **Cách kiểm tra:** Xác nhận `.env.example` chỉ thêm biến tên; log không in key/prompt raw, report phân biệt evaluator failure với answer failure.
- **Definition of Done:** Không chặn tiến độ khi thiếu credential; framework lựa chọn và limitation được ghi vào ADR.
- **Commit message gợi ý:** `test(rag): add optional grounded answer evaluator`
- **Câu hỏi tự kiểm tra:** Faithfulness khác answer relevancy thế nào? Vì sao CI không nên phụ thuộc hoàn toàn LLM judge?

### Ngày 27 — Error analysis và báo cáo tháng

- **Mục tiêu cụ thể:** Biến số liệu thành quyết định kỹ thuật nhỏ có bằng chứng.
- **Kết quả cần đạt:** `evals/rag/reports/month-04.md` có baseline/hybrid table, metric, threshold, latency/cost, 3–5 lỗi phân loại và next action có giới hạn.
- **Phân bổ thời gian:** 20 phút đọc report, 35 phút phân loại failure, 35 phút viết report, 20 phút review (110 phút).
- **Lý thuyết cần học:** Failure taxonomy: parsing/chunking, embedding/retrieval, fusion/rerank, context truncation, generation/citation, refusal và evaluator issue.
- **Tài liệu cần đọc:** RAGAS [Metrics](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/) — diễn giải hạn chế; xem lại report artifacts ngày 24–27.
- **Bài thực hành:** Chọn sample failure theo case ID, ghi observed/expected/root cause hypothesis/action; không cherry-pick chỉ case tốt.
- **Tích hợp project:** Ghi một thay đổi ưu tiên cho backlog (ví dụ sửa heading metadata) nhưng không mở feature lớn trong ngày review.
- **File tạo/sửa:** `evals/rag/reports/month-04.md`, `docs/adr/0004-rag-retrieval-decision.md`.
- **Lệnh chạy:** `uv run python evals/rag/run_rag_eval.py --config dense`; `uv run python evals/rag/run_rag_eval.py --config hybrid_rerank --compare dense`.
- **Kết quả mong đợi:** Report nói rõ cấu hình nào được chọn cho default và lý do/giới hạn; report không kết luận từ một metric.
- **Cách kiểm tra:** Mỗi assertion trong report link tới artifact/case ID; peer/self review kiểm tra no-answer và regression case có mặt.
- **Definition of Done:** Có baseline trước/sau, error analysis và decision có thể đảo lại khi dataset thay đổi.
- **Commit message gợi ý:** `docs(rag): publish retrieval evaluation analysis and decision`
- **Câu hỏi tự kiểm tra:** Một low faithfulness case cần debug bước nào đầu? Khi nào không nên đổi default dù metric tăng nhẹ?

### Ngày 28 — Milestone: end-to-end RAG demo, review và handoff

- **Mục tiêu cụ thể:** Chạy demo có kiểm soát từ ingest tới report, review quality gate và bàn giao capability RAG sang Month-05.
- **Kết quả cần đạt:** Script documented thực hiện ingest fixture, dense/hybrid search, grounded answer/refusal và evaluation artifact; `docs/month-05-handoff.md` ghi read-only contract/citation/timeout.
- **Phân bổ thời gian:** 15 phút chuẩn bị, 45 phút end-to-end run, 25 phút integration/regression test, 20 phút review/handoff (105 phút).
- **Lý thuyết cần học:** Demo khác production: mục tiêu là reproducibility và evidence, không benchmark vô hạn hay upload file bất kỳ.
- **Tài liệu cần đọc:** Qdrant [Quickstart](https://python-client.qdrant.tech/quickstart) — local connection; xem lại `RESOURCES.md` Tuần 2–4.
- **Bài thực hành:** Viết PowerShell-friendly runbook: khởi động Qdrant, ingest allowlisted fixture, chạy tests/eval, tắt service không xóa volume; ghi handoff cho graph chỉ-đọc.
- **Tích hợp project:** Thêm `scripts/demo_rag.ps1` hoặc `docs/rag-demo.md`; endpoint trả request id/citation/status, không trả internal scores mặc định; Month-05 chỉ gọi RAG như dependency.
- **File tạo/sửa:** `docs/rag-demo.md`, `docs/month-05-handoff.md`, `scripts/demo_rag.ps1`, `tests/integration/test_rag_e2e.py`.
- **Lệnh chạy:** `docker compose up -d qdrant`; `uv run pytest tests/integration/test_rag_e2e.py tests/evaluation/test_rag_regression.py -q`.
- **Kết quả mong đợi:** Một question grounded trả citation, one no-answer trả refusal, và report path được in không chứa secret.
- **Cách kiểm tra:** Chạy demo hai lần với corpus/config cố định; compare chunk IDs/retrieval config và kiểm tra commands không có destructive collection delete.
- **Definition of Done:** E2E test có thể skip khi Qdrant chưa chạy với hướng dẫn rõ; regression unit tests vẫn chạy offline; handoff không cho graph upsert/delete hay bypass citation policy.
- **Commit message gợi ý:** `docs(rag): hand off reproducible evaluated retrieval to agents`
- **Câu hỏi tự kiểm tra:** Demo có chứng minh production readiness không? Agent Month-05 cần nhận field nào từ RAG? Những phần nào phải fake để test ổn định?

## Milestone cuối tuần

Có golden dataset versioned, report dense so với hybrid+rerank, regression gate offline, một LLM evaluator tùy chọn, error analysis và demo tái lập được. Default retrieval được chọn bởi bằng chứng, không bởi cảm giác.

## Review checklist

- [ ] Dataset có question, expected chunk/source, category và no-answer cases.
- [ ] Dense và hybrid+rerank chạy trên cùng corpus/dataset/config record.
- [ ] Report có retrieval metrics, answer-grounding signal, latency và failure taxonomy.
- [ ] Deterministic regression test không cần API key/network.
- [ ] Chỉ một trong RAGAS/DeepEval là yêu cầu bắt buộc; thiếu credential được xử lý rõ.
- [ ] Handoff Month-05 mô tả RAG read-only capability, citation/refusal boundary và timeout.

## Definition of Done tuần

Evaluation chạy lại được và ghi report; ít nhất hai retrieval configuration được so sánh; quality gate có threshold hợp lý và error analysis. Handoff không thay đổi Month-05 hay giới thiệu agent sớm.

## Lỗi thường gặp

- Tự tạo golden answers bằng model rồi dùng chúng làm truth không review.
- So sánh hai config trên corpus/dataset khác nhau.
- Chỉ báo average score, không lưu per-case failure hay latency.
- Xem LLM judge là ground truth hoặc bắt CI gọi API có secret.

## Tài liệu tham khảo chính thức

Xem nhóm Tuần 04 trong [RESOURCES.md](./RESOURCES.md), cùng các link trực tiếp nêu theo từng ngày.

## Tùy chọn nếu còn thời gian

Thêm dashboard HTML từ JSON report hoặc đánh giá sensitivity với chunk size khác, nhưng chỉ sau khi baseline, gate và handoff đã hoàn thành.
