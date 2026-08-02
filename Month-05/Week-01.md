# Tháng 5 - Tuần 1: Workflow xác định, state và routing

## Mục tiêu tuần

Chuyển RAG pipeline tháng 4 thành LangGraph workflow nhỏ có state có kiểu, node độc lập, edge rõ ràng và conditional routing. Tuần này cố ý ưu tiên workflow xác định; LLM không được tự lặp công cụ.

## Kiến thức cần đạt

- Tool calling là model đề xuất/gọi tool trong một loop do ứng dụng kiểm soát; agent là workflow nhiều bước có state và quyết định bước tiếp theo.
- `StateGraph` gồm state dùng chung, node trả state update, fixed edge và conditional edge.
- Một graph phải có điều kiện dừng và nhánh lỗi; một câu hỏi không cần nhiều bước thì không nên dùng agent.

## Tính năng project sẽ bổ sung

Tạo `src/ai_assistant_platform/agents/` và endpoint draft `POST /api/v1/agent/runs`. Graph route query an toàn sang direct answer hoặc retrieval rồi draft có citations.

## Kế hoạch từng ngày

### Ngày 1 - Chọn đúng boundary cho agent

- **Mục tiêu cụ thể:** Viết quyết định kiến trúc phân biệt RAG pipeline, tool calling và agent workflow.
- **Kết quả cần đạt:** Có bảng quyết định: FAQ đơn giản dùng chat/RAG hiện có; research có kiểm tra citation dùng graph; export report sẽ cần approval ở tuần 3.
- **Phân bổ thời gian:** 20 phút ôn Month-04, 25 phút đọc, 45 phút viết ADR/diagram, 15 phút review (105 phút).
- **Nội dung lý thuyết:** Workflow có đường đi định trước khác agent routing động; không dùng agent chỉ để gọi một hàm retrieval.
- **Tài liệu cần đọc:** “Workflows and agents” trong [RESOURCES.md](./RESOURCES.md).
- **Bài thực hành:** Vẽ Mermaid `classify -> retrieve? -> draft -> review -> END`; ghi input/output cho từng node.
- **Thay đổi cần áp dụng vào ai-assistant-platform:** Thêm `docs/adr/005-agent-boundary.md`; giữ endpoint RAG cũ làm baseline.
- **File dự kiến tạo hoặc sửa:** `docs/adr/005-agent-boundary.md`, `docs/architecture/agent-workflow.md`.
- **Lệnh chạy:** `git diff --check`.
- **Kết quả mong đợi:** Diagram có đúng một `START`, một `END`, và không có hành động ghi/xoá dữ liệu.
- **Cách kiểm tra kết quả:** Đọc từng route và chỉ ra ai gọi tool, dữ liệu nào qua state, khi nào graph dừng.
- **Definition of Done:** ADR nêu ít nhất hai trường hợp *không* dùng agent và liên kết đến RAG evaluation Month-04.
- **Commit message gợi ý:** `docs(agent): define workflow boundary and routing design`
- **Câu hỏi tự kiểm tra:** Tool calling có tự tạo persistence không? Vì sao FAQ một lượt không cần graph?

### Ngày 2 - Khai báo AgentState có kiểu

- **Mục tiêu cụ thể:** Tạo state tối thiểu, serializable cho research workflow.
- **Kết quả cần đạt:** `AgentState` có `messages`, `query`, `route`, `documents`, `draft`, `citations`, `step_count`, `tool_calls_used`, `errors`.
- **Phân bổ thời gian:** 20 phút đọc, 55 phút code, 20 phút test schema, 10 phút ghi chú (105 phút).
- **Nội dung lý thuyết:** State là snapshot chia sẻ; node trả phần update thay vì mutate object toàn cục. Chỉ lưu dữ liệu JSON-serializable để checkpoint được.
- **Tài liệu cần đọc:** “State” và “Nodes” trong Graph API overview ở [RESOURCES.md](./RESOURCES.md).
- **Bài thực hành:** Dùng `TypedDict`/Pydantic boundary phù hợp codebase; tạo factory state từ `AgentRunRequest` đã validate.
- **Thay đổi cần áp dụng vào ai-assistant-platform:** Thêm `src/ai_assistant_platform/agents/state.py` và schema request/response cho run id/thread id.
- **File dự kiến tạo hoặc sửa:** `src/ai_assistant_platform/agents/state.py`, `src/ai_assistant_platform/api/schemas/agent.py`, `tests/unit/test_agent_state.py`.
- **Lệnh chạy:** `uv run pytest tests/unit/test_agent_state.py`.
- **Kết quả mong đợi:** Test từ chối query rỗng và state khởi tạo có `step_count=0`.
- **Cách kiểm tra kết quả:** Serialize state ra JSON; không có client, API key hoặc object database trong state.
- **Definition of Done:** State có type annotation cho mọi key và test pass.
- **Commit message gợi ý:** `feat(agent): add typed research workflow state`
- **Câu hỏi tự kiểm tra:** Vì sao không đưa OpenAI client vào state? Node cần trả toàn bộ state hay chỉ update?

### Ngày 3 - Node classify và fixed edge đầu tiên

- **Mục tiêu cụ thể:** Thêm node phân loại nhu cầu retrieval bằng rule xác định.
- **Kết quả cần đạt:** Query chứa yêu cầu nguồn/tài liệu được gán route `retrieve`; greeting hoặc câu hỏi ngoài knowledge base gán `direct`/`refuse` theo policy.
- **Phân bổ thời gian:** 15 phút đọc, 55 phút code, 25 phút unit test, 10 phút commit note (105 phút).
- **Nội dung lý thuyết:** Node là function dễ test; logic route ban đầu dùng rule để kiểm soát baseline trước khi để LLM quyết định.
- **Tài liệu cần đọc:** Ví dụ `StateGraph`, `START` và normal edge trong Graph API overview.
- **Bài thực hành:** Viết `classify_request(state)` và compile graph `START -> classify -> END`.
- **Thay đổi cần áp dụng vào ai-assistant-platform:** Thêm `src/ai_assistant_platform/agents/nodes.py`, `src/ai_assistant_platform/agents/graph.py` và fake direct reply node.
- **File dự kiến tạo hoặc sửa:** `src/ai_assistant_platform/agents/nodes.py`, `src/ai_assistant_platform/agents/graph.py`, `tests/unit/test_agent_routing.py`.
- **Lệnh chạy:** `uv run pytest tests/unit/test_agent_routing.py -k classify`.
- **Kết quả mong đợi:** Ba fixture query luôn ra route dự kiến, không gọi LLM hay Qdrant.
- **Cách kiểm tra kết quả:** Đếm mock retrieval client: bằng 0 với cả ba case.
- **Definition of Done:** Graph compile và node không có side effect.
- **Commit message gợi ý:** `feat(agent): add deterministic request classification node`
- **Câu hỏi tự kiểm tra:** Khi nào rule-based route tốt hơn LLM classifier? Fixed edge khác conditional edge thế nào?

### Ngày 4 - Conditional routing đến retrieval hoặc direct answer

- **Mục tiêu cụ thể:** Nối node classify với nhánh thích hợp và kết thúc rõ ràng.
- **Kết quả cần đạt:** `add_conditional_edges` route `retrieve`, `direct` hoặc `refuse`; mọi giá trị route khác đi qua node lỗi an toàn.
- **Phân bổ thời gian:** 20 phút đọc, 50 phút code, 25 phút test graph, 15 phút cập nhật diagram (110 phút).
- **Nội dung lý thuyết:** Conditional edge chỉ quyết định đường đi; tránh trộn normal edge và dynamic routing trên cùng node.
- **Tài liệu cần đọc:** Phần “Conditional edges” của Graph API overview trong [RESOURCES.md](./RESOURCES.md).
- **Bài thực hành:** Gắn adapter gọi retrieval service Month-04, giữ citation payload và tạo `direct_answer` stub.
- **Thay đổi cần áp dụng vào ai-assistant-platform:** Agent tái sử dụng service hybrid retrieval/reranker, không sao chép thuật toán RAG.
- **File dự kiến tạo hoặc sửa:** `src/ai_assistant_platform/agents/graph.py`, `src/ai_assistant_platform/agents/nodes.py`, `tests/unit/test_agent_routing.py`.
- **Lệnh chạy:** `uv run pytest tests/unit/test_agent_routing.py`.
- **Kết quả mong đợi:** Test chứng minh query research gọi retrieval đúng một lần; direct/refuse không gọi retrieval.
- **Cách kiểm tra kết quả:** Assert `route` cuối, docs/citations ở nhánh retrieve và error message không lộ internals ở nhánh refuse.
- **Definition of Done:** Không có route không xử lý hoặc vòng lặp vô hạn.
- **Commit message gợi ý:** `feat(agent): route research queries through retrieval graph branch`
- **Câu hỏi tự kiểm tra:** Vì sao một conditional function phải trả giá trị hữu hạn? Điều gì xảy ra nếu gắn cả fixed và conditional edge?

### Ngày 5 - Draft và review citation

- **Mục tiêu cụ thể:** Tách sinh câu trả lời khỏi kiểm tra citation.
- **Kết quả cần đạt:** Node `draft_answer` dùng context Month-04; node `review_answer` xác nhận nhánh retrieval có ít nhất một citation hợp lệ trước `finalize`.
- **Phân bổ thời gian:** 20 phút đọc lại contract RAG, 50 phút code, 30 phút test, 10 phút ghi chú (110 phút).
- **Nội dung lý thuyết:** Tách node giảm lỗi: generator không tự chứng nhận đầu ra; review ở đây là validation xác định, không phải LLM judge.
- **Tài liệu cần đọc:** “Nodes” và workflow routing examples trong [RESOURCES.md](./RESOURCES.md).
- **Bài thực hành:** Tạo `CitationMissingError`/result an toàn thay vì bịa nguồn; direct answer không được tự thêm citation giả.
- **Thay đổi cần áp dụng vào ai-assistant-platform:** Graph trả `AgentRunResponse` cùng `answer`, `citations`, `status`.
- **File dự kiến tạo hoặc sửa:** `src/ai_assistant_platform/agents/nodes.py`, `src/ai_assistant_platform/api/schemas/agent.py`, `tests/unit/test_agent_review.py`.
- **Lệnh chạy:** `uv run pytest tests/unit/test_agent_review.py`.
- **Kết quả mong đợi:** Draft có context pass; draft retrieval thiếu citation bị `blocked` thay vì trả lời tự tin.
- **Cách kiểm tra kết quả:** Dùng fixture citation ID không tồn tại và assert trạng thái `needs_retrieval`/`blocked`.
- **Definition of Done:** Citation validation dùng document IDs từ Month-04, không tin chuỗi URL do model sinh.
- **Commit message gợi ý:** `feat(agent): validate retrieval citations before final response`
- **Câu hỏi tự kiểm tra:** Tại sao citation review không nên nằm chung trong prompt draft? Direct answer có được gắn citation không?

### Ngày 6 - Milestone: API chạy graph một lượt

- **Mục tiêu cụ thể:** Expose graph qua API mà không thêm persistence hay tool loop.
- **Kết quả cần đạt:** `POST /api/v1/agent/runs` nhận query/thread id, trả route, answer/citations, status và step count.
- **Phân bổ thời gian:** 15 phút đọc API boundary, 60 phút tích hợp, 30 phút integration test, 15 phút smoke test (120 phút).
- **Nội dung lý thuyết:** HTTP route chỉ convert schema và gọi service; state graph không phụ thuộc FastAPI request object.
- **Tài liệu cần đọc:** LangGraph overview example trong [RESOURCES.md](./RESOURCES.md).
- **Bài thực hành:** Tiêm compiled graph qua dependency; mapping exception sang response contract hiện có.
- **Thay đổi cần áp dụng vào ai-assistant-platform:** Thêm agent route vào app main/router registration.
- **File dự kiến tạo hoặc sửa:** `src/ai_assistant_platform/api/routes/agent.py`, `src/ai_assistant_platform/api/dependencies.py`, `src/ai_assistant_platform/main.py`, `tests/integration/test_agent_api.py`.
- **Lệnh chạy:** `uv run pytest tests/integration/test_agent_api.py`; `uv run uvicorn ai_assistant_platform.main:app --reload`.
- **Kết quả mong đợi:** Swagger hiển thị endpoint; research fixture trả citations, greeting không gọi retrieval.
- **Cách kiểm tra kết quả:** Gọi endpoint bằng test client; assert response không chứa internal state hoặc stack trace.
- **Definition of Done:** Integration test pass và endpoint có response model.
- **Commit message gợi ý:** `feat(api): expose deterministic research agent run endpoint`
- **Câu hỏi tự kiểm tra:** Vì sao chưa gọi đây là agent tự trị? API response nên ẩn state keys nào?

### Ngày 7 - Review/buffer: củng cố workflow tuần 1

- **Mục tiêu cụ thể:** Rà graph, test nhánh và ghi handoff cho persistence tuần 2.
- **Kết quả cần đạt:** Mermaid diagram khớp code; test suite tuần 1 pass; backlog giới hạn còn checkpoint/thread memory.
- **Phân bổ thời gian:** 20 phút review diff, 30 phút chạy test, 25 phút refactor nhỏ, 15 phút ghi handoff (90 phút).
- **Nội dung lý thuyết:** Deterministic workflow là baseline để đo routing và latency trước khi thêm state liên phiên.
- **Tài liệu cần đọc:** Xem lại “Workflows and agents” trong [RESOURCES.md](./RESOURCES.md), chỉ phần phân biệt khái niệm.
- **Bài thực hành:** Xoá import chết, đặt hằng số route, thêm test unknown route và cập nhật architecture doc.
- **Thay đổi cần áp dụng vào ai-assistant-platform:** Tạo `docs/month-05-week-01-handoff.md` ghi state cần checkpoint và contract API hiện tại.
- **File dự kiến tạo hoặc sửa:** `src/ai_assistant_platform/agents/graph.py`, `tests/unit/test_agent_routing.py`, `docs/month-05-week-01-handoff.md`.
- **Lệnh chạy:** `uv run pytest tests/unit/test_agent_routing.py tests/unit/test_agent_review.py tests/integration/test_agent_api.py`; `uv run ruff check .`.
- **Kết quả mong đợi:** Toàn bộ lệnh pass; không có `TODO` như route placeholder.
- **Cách kiểm tra kết quả:** So diagram với `add_node`/`add_edge`; kiểm tra mỗi nhánh tới `END` hoặc lỗi an toàn.
- **Definition of Done:** Có thể giải thích state, node, edge và conditional route bằng chính graph vừa viết.
- **Commit message gợi ý:** `refactor(agent): review deterministic workflow baseline`
- **Câu hỏi tự kiểm tra:** Week 2 cần lưu state nào? Vì sao không checkpoint client object? Những nhánh nào cần metric baseline?

## Milestone cuối tuần

Agent route được query sang direct, retrieve hoặc refuse một cách xác định; response RAG chỉ hoàn tất khi citation hợp lệ. Unit và integration test chứng minh đường đi, không chỉ test text output.

## Review checklist

- [ ] Có định nghĩa rõ tool calling vs agent trong ADR.
- [ ] `AgentState` serializable và không chứa secret/client.
- [ ] Mỗi route kết thúc hoặc báo lỗi an toàn.
- [ ] Retrieval tái sử dụng module Month-04.
- [ ] Nhánh RAG kiểm citation bằng ID đáng tin cậy.
- [ ] Endpoint có response model và integration test.

## Definition of Done tuần

Graph compile được; routing, citation review và API test pass; diagram/ADR khớp implementation; không có persistence hay sensitive side effect bị thêm sớm.

## Lỗi thường gặp

- Coi mọi `if/else` là agent rồi thêm LangGraph không có giá trị.
- Mutate state toàn cục hoặc nhét object không serialize được vào checkpoint tương lai.
- Cho LLM tự sinh citation URL thay vì giữ ID document.
- Để route lạ rơi qua default answer thay vì fail closed.

## Tùy chọn nếu còn thời gian

Render Mermaid graph trong test/docs. Không thêm LLM routing, tool execution hay memory trước tuần sau.
