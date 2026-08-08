## Run

```powershell
uv run python -m ai_assistant_platform.main
```

## Run test

```powershell
uv run pytest
```

## Run lint and format

```powershell
uv run ruff check --fix
uv run ruff format
```

## OpenAPI Schema

- Swagger UI: http://localhost:8001/docs
- OpenAPI JSON: http://localhost:8001/openapi.json

## Example Request

```powershell
curl -X POST "http://localhost:8001/api/v1/chat" -H "Content-Type: application/json" -d "{\"content\": \"Hello\"}"
```
