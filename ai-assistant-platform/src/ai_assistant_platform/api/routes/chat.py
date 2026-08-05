from fastapi import APIRouter

from ai_assistant_platform.api.schemas import ChatRequest, ChatResponse
from ai_assistant_platform.domain.chat import ChatMessage
from ai_assistant_platform.services import build_mock_reply

router = APIRouter(
    prefix="/api/v1",
    tags=["chatbot"],
    responses={418: {"description": "I'm a teapot"}},
)


@router.post("/chat")
def chat(request: ChatRequest) -> ChatResponse:
    # 1. Map từ API Schema -> Domain Model
    domain_message = ChatMessage("user", request.content)

    # 2. Gọi Service với Domain Model
    reply = build_mock_reply(domain_message)

    # 3. Trả về API Response Schema
    return ChatResponse(reply=reply)
