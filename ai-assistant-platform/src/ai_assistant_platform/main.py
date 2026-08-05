"""Application entry point for the AI assistant platform."""

import uvicorn
from fastapi import FastAPI

from ai_assistant_platform.api.routes.chat import router as chat_router
from ai_assistant_platform.api.routes.health import router as health_router
from ai_assistant_platform.core.logging import setup_logging

app = FastAPI()
app.include_router(health_router)
app.include_router(chat_router)


def main() -> None:
    """Initialize logging and start the AI assistant platform."""
    setup_logging()
    print("ai-assistant-platform ready")
    uvicorn.run(
        "ai_assistant_platform.main:app", host="127.0.0.1", port=8001, reload=True
    )


if __name__ == "__main__":
    main()
