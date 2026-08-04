# Tháng 03 — Tuần 02: Prompt, Structured Output và prompt regression

## Mục tiêu tuần

Thiết kế prompt theo contract, trả dữ liệu có cấu trúc qua Pydantic và tạo bộ regression nhỏ đo hành vi thay vì so khớp nguyên văn câu trả lời.

## Kiến thức và feature sẽ bổ sung

- System/developer instruction, user input, few-shot example và boundary chống prompt injection cơ bản.
- Structured Output JSON schema, Pydantic validation, fallback không bịa dữ liệu.
- `src/ai_assistant_platform/domain/support.py`, `src/ai_assistant_platform/services/structured_answer_service.py`, fixtures/dataset regression và report JSON.

## Kế hoạch từng ngày

### Ngày 08 — Prompt contract và instruction hierarchy

**Tài liệu:** đọc [Responses API reference](https://platform.openai.com/docs/api-reference/responses), phần `instructions` và input roles.

- **Mục tiêu:** viết prompt template một nguồn sự thật.
- **Kết quả cần đạt:** `SupportPromptBuilder` tách policy, context và câu hỏi người dùng.
- **Thời lượng (90 phút):** 25 phút đọc roles trong Responses reference, 40 phút code, 15 phút test, 10 phút ghi chú.
- **Lý thuyết:** instruction ưu tiên hơn user input; prompt không phải nơi cấp quyền tool.
- **Bài thực hành:** viết policy yêu cầu nêu unknown thay vì đoán.
- **Tích hợp project:** `ChatService` nhận prompt từ builder.
- **File:** `src/ai_assistant_platform/llm/prompts/support.py`, `tests/unit/test_support_prompt.py`.
- **Lệnh:** `uv run pytest tests/unit/test_support_prompt.py -q`.
- **Kết quả mong đợi:** user text được đóng trong section riêng, không concat vào policy.
- **Kiểm tra:** input “bỏ qua chỉ dẫn” không làm thay đổi template policy.
- **DoD:** prompt version có tên, ví dụ `support-v1`.
- **Commit:** `feat(prompt): add versioned support prompt builder`.
- **Tự kiểm tra:** System instruction giải quyết được gì và không giải quyết được gì? Vì sao policy không lấy từ request?

### Ngày 09 — Few-shot tối thiểu và rubric

**Tài liệu:** xem [OpenAI prompting guide](https://platform.openai.com/docs/guides/prompting), phần examples và evaluation.

- **Mục tiêu:** thêm ví dụ chỉ cho format khó, không nhồi lịch sử chat.
- **Kết quả cần đạt:** hai few-shot case minh họa answer có căn cứ và unknown.
- **Thời lượng (85 phút):** 20 phút lý thuyết, 40 phút prompt/test, 15 phút review token budget, 10 phút ghi chú.
- **Lý thuyết:** example là specification mềm, tăng token/cost.
- **Bài thực hành:** thêm `examples` immutable, kiểm tra thứ tự.
- **Tích hợp project:** prompt v1 đưa examples khi gọi structured endpoint.
- **File:** `src/ai_assistant_platform/llm/prompts/examples.py`, `tests/unit/test_prompt_examples.py`.
- **Lệnh:** `uv run pytest tests/unit/test_prompt_examples.py -q`.
- **Kết quả mong đợi:** example không chứa dữ liệu người dùng thật.
- **Kiểm tra:** count examples=2 và input mới không thay example.
- **DoD:** ghi lý do giữ mỗi example trong code comment ngắn.
- **Commit:** `feat(prompt): add focused few-shot examples`.
- **Tự kiểm tra:** Khi nào few-shot làm hại latency? Ví dụ khác instruction ở điểm nào?

### Ngày 10 — Pydantic schema cho Structured Output

**Tài liệu:** đọc [Pydantic models](https://docs.pydantic.dev/latest/concepts/models/), phần field validation và JSON Schema.

- **Mục tiêu:** xác định contract answer trước khi gọi model.
- **Kết quả cần đạt:** `SupportAnswer` gồm `answer`, `confidence` 0–1, `needs_human_review`, `reason_codes`.
- **Thời lượng (100 phút):** 20 phút đọc Pydantic models, 55 phút schema/test, 15 phút inspect JSON schema, 10 phút ghi chú.
- **Lý thuyết:** validation schema vs semantic truth.
- **Bài thực hành:** constraint độ dài answer và enum reason code.
- **Tích hợp project:** schema thuộc `src/ai_assistant_platform/domain`, không thuộc route.
- **File:** `src/ai_assistant_platform/domain/support.py`, `tests/unit/test_support_schema.py`.
- **Lệnh:** `uv run pytest tests/unit/test_support_schema.py -q`.
- **Kết quả mong đợi:** invalid confidence/reason bị từ chối.
- **Kiểm tra:** chạy `uv run python -c "from ai_assistant_platform.domain.support import SupportAnswer; print(SupportAnswer.model_json_schema())"`.
- **DoD:** schema có mô tả field hỗ trợ model.
- **Commit:** `feat(schema): define structured support answer`.
- **Tự kiểm tra:** Schema hợp lệ có bảo đảm câu trả lời đúng không? Field nào cần enum?

### Ngày 11 — Parse structured output và fallback

**Tài liệu:** xem [OpenAI Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs), phần schema và refusal/error handling.

- **Mục tiêu:** xử lý output không parse được mà không trả JSON nửa vời.
- **Kết quả cần đạt:** service trả `StructuredAnswerResult` có `status=valid|fallback`; fallback nêu rõ không thể cấu trúc hóa.
- **Thời lượng (105 phút):** 25 phút đọc Structured Outputs/reference, 50 phút code, 20 phút test, 10 phút ghi chú.
- **Lý thuyết:** provider-enforced schema vẫn cần boundary validation.
- **Bài thực hành:** fake trả JSON hỏng và JSON sai enum.
- **Tích hợp project:** service không retry vô điều kiện khi validation fail.
- **File:** `src/ai_assistant_platform/services/structured_answer_service.py`, `src/ai_assistant_platform/llm/structured_parser.py`, `tests/unit/test_structured_answer_service.py`.
- **Lệnh:** `uv run pytest tests/unit/test_structured_answer_service.py -q`.
- **Kết quả mong đợi:** hai fixture hỏng tạo fallback an toàn.
- **Kiểm tra:** API không trả traceback/partial object.
- **DoD:** log chỉ chứa error category và request id.
- **Commit:** `feat(llm): validate structured answers with fallback`.
- **Tự kiểm tra:** Vì sao validation cần tồn tại dù provider hỗ trợ structured output? Khi nào nên gửi lại yêu cầu sửa format?

### Ngày 12 — Structured endpoint và response contract

**Tài liệu:** đọc [FastAPI response model](https://fastapi.tiangolo.com/tutorial/response-model/), phần response validation.

- **Mục tiêu:** expose endpoint ổn định cho client.
- **Kết quả cần đạt:** `POST /api/v1/support/answer` trả `SupportAnswerResponse` rõ valid/fallback.
- **Thời lượng (95 phút):** 15 phút thiết kế HTTP contract, 50 phút route/test, 20 phút manual verification, 10 phút ghi chú.
- **Lý thuyết:** response model tách domain/provider representation.
- **Bài thực hành:** inject fake structured service trong integration test.
- **Tích hợp project:** thêm router mà không sửa `/chat` contract.
- **File:** `src/ai_assistant_platform/api/routes/support.py`, `src/ai_assistant_platform/api/schemas/support.py`, `src/ai_assistant_platform/main.py`, `tests/integration/test_support_api.py`.
- **Lệnh:** `uv run pytest tests/integration/test_support_api.py -q`.
- **Kết quả mong đợi:** 200 valid response và fallback shape ổn định.
- **Kiểm tra:** malformed user request trả 422, không đến LLM.
- **DoD:** endpoint docs mô tả fallback.
- **Commit:** `feat(api): expose structured support answer`.
- **Tự kiểm tra:** Vì sao fallback vẫn có 200 trong contract này? Client biết lúc nào cần human review thế nào?

### Ngày 13 — Dataset và prompt regression test

**Tài liệu:** xem [OpenAI evals guide](https://platform.openai.com/docs/guides/evals), phần thiết kế test case và grader có kiểm soát.

- **Mục tiêu:** biến mong đợi prompt thành data versioned.
- **Kết quả cần đạt:** ít nhất 6 case gồm happy path, unknown, injection attempt và invalid-shape fixture.
- **Thời lượng (100 phút):** 20 phút chọn cases, 50 phút fixture/runner, 20 phút test, 10 phút ghi chú.
- **Lý thuyết:** regression test khác unit test; không assert exact prose.
- **Bài thực hành:** mỗi case có input, expected flags/reason và `prompt_version`.
- **Tích hợp project:** `tests/evaluation/prompt_cases.json` dùng fake deterministic.
- **File:** `tests/evaluation/prompt_cases.json`, `tests/evaluation/test_prompt_regression.py`, `tests/fixtures/llm/`.
- **Lệnh:** `uv run pytest tests/evaluation/test_prompt_regression.py -q`.
- **Kết quả mong đợi:** fail report nêu case id/expected/actual.
- **Kiểm tra:** cố ý đổi expected flag để thấy failure hữu ích.
- **DoD:** dataset không chứa PII/secret.
- **Commit:** `test(prompt): add structured output regression cases`.
- **Tự kiểm tra:** Vì sao không so sánh toàn bộ answer text? Case injection kiểm tra điều gì?

### Ngày 14 — Baseline, threshold và review

**Tài liệu:** đọc [OpenAI evaluation best practices](https://platform.openai.com/docs/guides/evals), tập trung vào baseline và error analysis.

- **Mục tiêu:** chốt baseline trước khi sửa prompt tiếp.
- **Kết quả cần đạt:** report có pass rate, schema-valid rate, fallback count và failure taxonomy; threshold ban đầu ghi rõ.
- **Thời lượng (100 phút):** 20 phút định metric, 40 phút report script, 25 phút chạy/sửa, 15 phút review.
- **Lý thuyết:** nhiều metric, baseline không phải production truth.
- **Bài thực hành:** runner ghi `artifacts/prompt-regression.json` (được `.gitignore` nếu là output runtime) hoặc snapshot fixture có chủ đích.
- **Tích hợp project:** README mô tả `uv run pytest tests/evaluation`.
- **File:** `scripts/run_prompt_regression.py`, `docs/prompt-regression-baseline.md`, `.gitignore`, `README.md`.
- **Lệnh:** `uv run python scripts/run_prompt_regression.py`; `uv run pytest tests/evaluation -q`.
- **Kết quả mong đợi:** baseline nêu `6/6` fixture pass và giới hạn của fake.
- **Kiểm tra:** case fail làm process exit code khác 0.
- **DoD:** không gọi API thật trong CI baseline.
- **Commit:** `test(prompt): document baseline and regression report`.
- **Tự kiểm tra:** Pass rate 100% trên fake nói lên điều gì? Metric nào cho thấy fallback tăng?

## Milestone, review và DoD

- **Milestone:** endpoint structured trả contract validated; 6 regression case chạy offline và có baseline.
- **Review checklist:** [ ] prompt versioned; [ ] Pydantic constraint có test; [ ] fallback không bịa data; [ ] dataset có adversarial case; [ ] metric không chỉ là pass/fail.
- **Definition of Done:** thay prompt phải cập nhật/đánh giá regression cases.
- **Lỗi thường gặp:** parse JSON bằng `dict` không validate, assert nguyên văn answer, đưa policy vào user message, log toàn bộ output.
- **Tùy chọn (≤30 phút):** thêm one-line changelog prompt version.
- **Tài liệu:** [README tháng](./README.md#tài-liệu-tham-khảo-đã-chọn), đặc biệt Pydantic và Responses reference.
