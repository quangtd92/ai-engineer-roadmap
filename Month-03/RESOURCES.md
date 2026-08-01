# Tháng 03 — Tài liệu tham khảo

Chỉ đọc phần được ghi ở từng ngày; tất cả nguồn dưới đây là tài liệu chính thức hoặc specification chính thức. Không cần API key để đọc hay chạy test bằng fake adapter.

## LLM, output và evaluation

- [OpenAI Responses API reference](https://platform.openai.com/docs/api-reference/responses) — request, output và `usage`.
- [OpenAI Responses streaming](https://platform.openai.com/docs/api-reference/responses-streaming) — event stream và lifecycle.
- [OpenAI Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs) — schema boundary.
- [OpenAI Evals guide](https://platform.openai.com/docs/guides/evals) — dataset, baseline và grader.
- [Pydantic models](https://docs.pydantic.dev/latest/concepts/models/) — validation và `ValidationError`.

## Tool Calling, MCP và API boundary

- [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling) — schema, tool call và tool result.
- [MCP server concepts](https://modelcontextprotocol.io/docs/learn/server-concepts) — server, tool, resource và security boundary.
- [MCP tools specification](https://modelcontextprotocol.io/specification/draft/server/tools) — contract tool.
- [MCP resources specification](https://modelcontextprotocol.io/specification/draft/server/resources) — resource read-only.
- [FastAPI error handling](https://fastapi.tiangolo.com/tutorial/handling-errors/) — HTTP error boundary.

## Tìm hiểu thêm

- [OpenAI safety best practices](https://platform.openai.com/docs/guides/safety-best-practices) — prompt injection và xử lý input không tin cậy.
- [Python asyncio timeout](https://docs.python.org/3/library/asyncio-task.html#asyncio.timeout) — timeout cho coroutine.
