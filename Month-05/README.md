# Tháng 5 — LangGraph Agent, Reliability và Human-in-the-loop

Tháng 5 biến RAG assistant của tháng 4 thành một workflow có trạng thái, có giới hạn và có người phê duyệt trước các hành động nhạy cảm. Mục tiêu không phải tạo agent tự trị vô hạn: workflow ưu tiên quyết định xác định, dữ liệu kiểm tra được và ranh giới quyền rõ ràng.

## Mục tiêu tháng

- Phân biệt tool calling (một vòng gọi công cụ do ứng dụng điều phối) với agent (vòng lặp chọn bước tiếp theo theo state và routing).
- Xây `StateGraph` với state có kiểu, node, edge, conditional routing và đường kết thúc rõ ràng.
- Lưu checkpoint theo `thread_id`; dùng short-term memory, đồng thời hiểu giới hạn của long-term memory.
- Dừng, hiển thị và chỉ tiếp tục hành động nhạy cảm sau approval; hỗ trợ approve, edit và reject.
- Áp dụng retry có giới hạn, timeout, max steps, tool budget, idempotency và error recovery.
- Thêm guardrail đầu vào/đầu ra, permission boundary, tracing bằng LangSmith và agent evaluation bằng DeepEval.

## Kiến thức đầu vào

Người học đã hoàn thành RAG tháng 4: ingest/chunk/metadata, hybrid retrieval, reranking, citation, prompt-injection defense cho tài liệu và dataset đánh giá. Cũng cần có OpenAI tool calling, Pydantic validation, timeout/retry và test từ tháng 3. Không bắt đầu tháng này nếu chat/RAG endpoint chưa chạy được.

## Kết quả đầu ra

`ai-assistant-platform` có một `research_agent` phục vụ truy vấn tài liệu nội bộ:

- Route câu hỏi sang trả lời trực tiếp, RAG retrieval hoặc một safe tool đã đăng ký.
- Có `AgentState`, các node `classify`, `retrieve`, `draft`, `review`, `request_approval` và `finalize` (có thể khác tên nhưng cùng trách nhiệm).
- Checkpoint theo `thread_id`, API đọc state và tiếp tục execution sau interrupt.
- `export_report` là hành động nhạy cảm: chỉ tạo file/ghi bản ghi sau quyết định phê duyệt được lưu audit log; không có tool xoá dữ liệu trong phạm vi tháng này.
- Có policy cho max 6 bước, tối đa 2 tool calls, timeout từng tool và retry chỉ cho lỗi transient.
- Có trace không chứa raw secret; dataset agent evaluation, baseline, threshold và report lỗi.

## Kiến trúc trước và sau tháng

Trước tháng 5, assistant có API LLM/tool calling và RAG có citation/evaluation, nhưng không lưu workflow state hoặc điều phối hành động đa bước.

```text
Trước: request -> RAG retrieve/rerank -> LLM answer + citations
```

Sau tháng 5:

```text
POST /api/v1/agent/runs
  -> StateGraph(classify -> retrieve? -> draft -> review)
  -> approval interrupt? -> resume -> finalize
  -> checkpoints + audit log + LangSmith trace
```

Các module đích (tên có thể điều chỉnh theo codebase hiện có):

```text
app/
├── agents/
│   ├── graph.py
│   ├── state.py
│   ├── nodes.py
│   ├── policies.py
│   ├── approval.py
│   └── tools.py
├── api/routes/agent.py
├── evaluation/agent_dataset.jsonl
├── observability/langsmith.py
└── services/checkpoints.py
tests/
├── unit/test_agent_routing.py
├── integration/test_agent_resume.py
└── evaluation/test_agent_eval.py
```

## Milestone từng tuần

| Tuần | Trọng tâm | Milestone kiểm tra được |
| --- | --- | --- |
| [Tuần 1](./Week-01.md) | Graph xác định, state và routing | Agent trả lời/truy xuất đúng nhánh, dừng hữu hạn và có unit test routing |
| [Tuần 2](./Week-02.md) | Checkpoint, persistence và memory | Hai request cùng `thread_id` khôi phục được context; restart mô phỏng không mất checkpoint |
| [Tuần 3](./Week-03.md) | HITL và reliability | Hành động export bị interrupt, approve/edit/reject có thể resume; retry/timeout/budget được test |
| [Tuần 4](./Week-04.md) | Guardrails, tracing và evaluation | Agent có policy boundary, trace an toàn, report so sánh baseline với cấu hình hiện tại |

## Nhịp học và command

Mỗi ngày 60–120 phút: một trọng tâm, khoảng 30% đọc/ghi chú và 70% code/test. Ngày 6, 13, 20 và 27 là milestone; ngày 7, 14, 21 và 28 là review/buffer. Lệnh Python dùng `uv run`; thay tên file/module nếu project thực tế dùng cấu trúc khác, nhưng giữ boundary tương đương.

```bash
uv add langgraph langsmith deepeval
uv run pytest tests/unit/test_agent_routing.py
uv run ruff check .
```

Không đưa `LANGSMITH_API_KEY`, OpenAI key hoặc URL Postgres thật vào Git. Dùng `.env.example` với tên biến và giá trị rỗng; log `thread_id` đã băm nếu có khả năng chứa định danh người dùng.

## Tài liệu tham khảo

Các link đã kiểm tra và phần đọc theo từng ngày nằm trong [RESOURCES.md](./RESOURCES.md). Không cần đọc toàn bộ tài liệu trong một lượt.

## Definition of Done tháng

- Hoàn thành 28 ngày ở bốn file tuần, mỗi ngày có đủ mục tiêu, output, thời lượng, lý thuyết, tài liệu, thực hành, project, file, lệnh, expected result, verification, DoD, commit và câu hỏi tự kiểm tra.
- Graph có state, node/edge, conditional route và test cho nhánh RAG, nhánh direct answer, nhánh tool/error.
- Có checkpoint/persistence với `thread_id`, short-term memory và tài liệu nêu rõ long-term memory chỉ là overview, chưa tự động ghi thông tin nhạy cảm.
- Sensitive action yêu cầu interrupt/resume và audit; người dùng có thể approve, edit hoặc reject.
- Retry/timeout/max steps/tool budget/idempotency có test pass/fail cụ thể.
- Guardrails chặn input vượt permission boundary và output thiếu citation trong nhánh RAG.
- Tracing được cấu hình opt-in, không log secret/raw authorization header; agent evaluation có dataset, baseline, nhiều metric, threshold và report.
- `uv run pytest`, `uv run ruff check .` pass; cập nhật `docs/month-06-handoff.md` cho bước production, không sửa nội dung Month-06.

## Rủi ro và cách giảm tải

- **Agent quá tự trị:** chỉ xây một graph phục vụ research assistant; không thêm multi-agent, browser automation hoặc tác vụ phá huỷ.
- **Persistence quá rộng:** dùng `InMemorySaver` cho test trước; Postgres/Redis chỉ là adapter mục tiêu, không cần vận hành cluster.
- **HITL lẫn với authentication:** approval là policy workflow, không thay thế phân quyền người dùng hoặc xác thực API.
- **Evaluation chỉ dùng LLM judge:** kết hợp assertion xác định (budget, route, tool args) với tool correctness/task completion và review lỗi thủ công.
- **Tracing làm lộ dữ liệu:** dùng input/output anonymization, metadata tối thiểu, tắt trace khi local nếu chưa có project LangSmith.

## Nội dung tùy chọn

Chỉ làm khi 28 ngày bắt buộc đã hoàn thành: semantic long-term memory có consent rõ ràng; replay checkpoint để debug; dashboard LangSmith. Không thêm framework agent thứ hai.

## Cầu nối sang Month-06

Month-06 đóng gói graph đã giới hạn và đã có test/evaluation vào Docker, CI/CD và AWS. Handoff cần liệt kê environment variables, migration/checkpointer được chọn, health/readiness cho dependency persistence, trace sampling và lệnh chạy evaluation; không đưa secret hoặc checkpoint thật vào repository.

## Review và điều hướng

- [Tuần 1 — Workflow xác định, state và routing](./Week-01.md)
- [Tuần 2 — Checkpoint, persistence và memory](./Week-02.md)
- [Tuần 3 — Human-in-the-loop và reliability](./Week-03.md)
- [Tuần 4 — Guardrails, tracing và evaluation](./Week-04.md)
- [Tài liệu tham khảo](./RESOURCES.md)
- [Báo cáo tự review Month-05](./REVIEW.md)
