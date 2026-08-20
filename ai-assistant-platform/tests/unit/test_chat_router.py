from ai_assistant_platform.api.routes.chat import chat
from ai_assistant_platform.api.schemas import ChatRequest, ChatResponse


def test_chat_route_handler():
    """Unit test: gọi trực tiếp hàm chat route handler."""
    request = ChatRequest(content="Hello World")
    response = chat(request)

    assert isinstance(response, ChatResponse)
    assert response.reply == "Mock reply to: Hello World"
