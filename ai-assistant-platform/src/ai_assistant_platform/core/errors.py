from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


class PlatformError(Exception):
    pass


class ValidationError(PlatformError):
    pass


class BaseException(Exception):
    pass


class NotFoundError(BaseException):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


class ExternalServiceError(BaseException):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


class LLMProviderError(BaseException):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


class InvalidMessageError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


async def not_found_error_handler(request: Request, exc: NotFoundError):
    return JSONResponse(
        status_code=404,
        content={"code": "NOT_FOUND_ERROR", "detail": exc.message},
    )


async def external_service_error_handler(request: Request, exc: ExternalServiceError):
    return JSONResponse(
        status_code=503,
        content={"code": "EXTERNAL_SERVICE_ERROR", "detail": exc.message},
    )


async def llm_provider_error_handler(request: Request, exc: LLMProviderError):
    return JSONResponse(
        status_code=502,
        content={"code": "LLM_PROVIDER_ERROR", "detail": exc.message},
    )


async def invalid_message_error_handler(request: Request, exc: InvalidMessageError):
    return JSONResponse(
        status_code=400,
        content={"code": "INVALID_MESSAGE", "detail": exc.message},
    )


async def validation_error_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
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
