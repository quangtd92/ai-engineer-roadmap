from ai_assistant_platform.domain.chat import ChatMessage

def build_mock_reply(message: ChatMessage) -> str:
    print("build_mock_reply", message)
    """
    Build a mock reply to a message.

    Args:
        message (ChatMessage): The message to reply to.

    Returns:
        str: The mock reply.
    """
    return f"Mock reply to: {message.content.strip()}"
