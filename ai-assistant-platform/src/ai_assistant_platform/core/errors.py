import logging

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


class PlatformError(Exception):
    """Base exception for all domain and platform errors."""

    def __init__(self, message: str = ""):
        super().__init__(message)
        self.message = message


class ValidationError(PlatformError):
    """Raised when data validation fails."""


class NotFoundError(PlatformError):
    """Raised when a requested resource is not found."""


class ExternalServiceError(PlatformError):
    """Raised when an external downstream service fails or times out."""


class LLMProviderError(PlatformError):
    """Raised when an LLM upstream provider encounters an error."""


class InvalidMessageError(PlatformError):
    """Raised when a chat message is invalid or rejected by domain rules."""


async def not_found_error_handler(request: Request, exc: NotFoundError):
    logger.error("Not found error: %s", exc)
    return JSONResponse(
        status_code=404,
        content={"code": "NOT_FOUND_ERROR", "detail": exc.message},
    )


async def external_service_error_handler(request: Request, exc: ExternalServiceError):
    logger.error("External service error: %s", exc)
    return JSONResponse(
        status_code=503,
        content={"code": "EXTERNAL_SERVICE_ERROR", "detail": exc.message},
    )


async def llm_provider_error_handler(request: Request, exc: LLMProviderError):
    logger.error("LLM provider error: %s", exc)
    return JSONResponse(
        status_code=502,
        content={"code": "LLM_PROVIDER_ERROR", "detail": exc.message},
    )


async def invalid_message_error_handler(request: Request, exc: InvalidMessageError):
    logger.error("Invalid message error: %s", exc)
    return JSONResponse(
        status_code=400,
        content={"code": "INVALID_MESSAGE", "detail": exc.message},
    )


async def validation_error_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    logger.error("Validation error: %s", exc)
    errors = [
        {
            "loc": list(error["loc"]),
            "msg": error["msg"],
            "type": error["type"],
        }
        for error in exc.errors()
    ]

    return JSONResponse(
        status_code=422,
        content={"code": "VALIDATION_ERROR", "detail": errors},
    )
