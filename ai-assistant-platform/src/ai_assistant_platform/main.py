"""Application entry point for the AI assistant platform."""

import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from ai_assistant_platform.api.routes.chat import router as chat_router
from ai_assistant_platform.api.routes.health import router as health_router
from ai_assistant_platform.core.errors import (
    ExternalServiceError,
    InvalidMessageError,
    LLMProviderError,
    NotFoundError,
    external_service_error_handler,
    invalid_message_error_handler,
    llm_provider_error_handler,
    not_found_error_handler,
    validation_error_handler,
)
from ai_assistant_platform.core.logging import setup_logging

app = FastAPI(
    title="AI Assistant Platform",
    version="1.0.0",
    description="AI Assistant Platform",
    tags=[
        {"name": "chat", "description": "Chat API"},
        {"name": "health", "description": "Health Check API"},
    ],
)
app.include_router(health_router)
app.include_router(chat_router)

app.add_exception_handler(RequestValidationError, validation_error_handler)
app.add_exception_handler(InvalidMessageError, invalid_message_error_handler)
app.add_exception_handler(NotFoundError, not_found_error_handler)
app.add_exception_handler(ExternalServiceError, external_service_error_handler)
app.add_exception_handler(LLMProviderError, llm_provider_error_handler)


def main() -> None:
    """Initialize logging and start the AI assistant platform."""
    setup_logging()
    print("ai-assistant-platform ready")
    uvicorn.run(
        "ai_assistant_platform.main:app", host="127.0.0.1", port=8001, reload=True
    )


if __name__ == "__main__":
    main()
