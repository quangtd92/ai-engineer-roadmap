from ai_assistant_platform.domain.chat import ChatMessage
from ai_assistant_platform.core.errors import InvalidMessageError
import logging

logger = logging.getLogger(__name__)

def build_mock_reply(message: ChatMessage) -> str:
    """
    Build a mock reply to a message.

    Args:
        message (ChatMessage): The message to reply to.

    Returns:
        str: The mock reply.
    """

    logger.info("start 111")
    content = message.content.strip()
    if not content:
        logger.warning("Attempted to process empty message content")
        raise InvalidMessageError("Content has to have value, not empty string")
    logger.info(f"Length Content: {len(content)}")
    return f"Mock reply to: {content}"

