from fastapi import APIRouter

from ai_assistant_platform.api.schemas import ChatRequest, ChatResponse
from ai_assistant_platform.api.schemas.errors import ErrorResponse
from ai_assistant_platform.domain.chat import ChatMessage
from ai_assistant_platform.services import build_mock_reply

router = APIRouter(
    prefix="/api/v1",
    tags=["chatbot"],
)


@router.post(
    "/chat",
    response_model=ChatResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid message"},
        422: {"model": ErrorResponse, "description": "Request validation error"},
    },
)
def chat(request: ChatRequest) -> ChatResponse:
    domain_message = ChatMessage("user", request.content)

    reply = build_mock_reply(domain_message)

    return ChatResponse(reply=reply)
