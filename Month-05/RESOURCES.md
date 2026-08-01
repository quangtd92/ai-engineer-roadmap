# Tháng 5 - Tài liệu tham khảo

Chỉ đọc phần gắn với ngày học. Các nguồn chính thức bên dưới đã được kiểm tra trước khi xuất bản.

## Tuần 1

- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview): vai trò orchestration runtime và ví dụ `StateGraph` tối thiểu.
- [Graph API overview](https://docs.langchain.com/oss/python/langgraph/graph-api): state, node, edge, `START`/`END`, conditional edge và `Command`.
- [Workflows and agents](https://docs.langchain.com/oss/python/langgraph/workflows-agents): phân biệt workflow có đường đi định trước với agent có routing động.

## Tuần 2

- [Persistence](https://docs.langchain.com/oss/python/langgraph/persistence): checkpoint, thread, state history và fault tolerance.
- [Memory](https://docs.langchain.com/oss/python/langgraph/add-memory): short-term/long-term memory, trimming và database setup.
- [LangGraph memory concepts](https://docs.langchain.com/oss/python/concepts/memory): phạm vi thread và namespace của memory.

## Tuần 3

- [Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts): pause/resume, `Command(resume=...)` và idempotency quanh side effect.
- [Human-in-the-loop](https://docs.langchain.com/oss/python/langchain/human-in-the-loop): approve, edit, reject và checkpointer cho interrupt.

## Tuần 4

- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview): liên hệ LangGraph với LangSmith debugging/tracing.
- [DeepEval agent evaluation quickstart](https://deepeval.com/docs/getting-started-agents): trace, component evaluation và end-to-end evaluation.
- [DeepEval tool correctness](https://deepeval.com/docs/metrics-tool-correctness): expected tools, threshold và mức strictness.
- [DeepEval task completion](https://deepeval.com/docs/metrics-task-completion): metric theo full trace và reason của evaluator.

## Tìm hiểu thêm

- [LangGraph Functional API](https://docs.langchain.com/oss/python/langgraph/functional-api): chọn Functional API khi cần thêm persistence vào code tuyến tính hiện có; không bắt buộc trong tháng này.
