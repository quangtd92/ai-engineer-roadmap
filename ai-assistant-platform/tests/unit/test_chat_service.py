from ai_assistant_platform.core.errors import InvalidMessageError
from ai_assistant_platform.domain.chat import ChatMessage
from ai_assistant_platform.services.chat_service import build_mock_reply
import pytest

class TestChatService:
    """
    Test chat service
    """

    # Mock data for testing
    @pytest.fixture
    def valid_chatbox(self):
        """Fixture for a valid chatbox"""
        return ChatMessage('Admin', 'Hello world!')

    @pytest.fixture
    def empty_chatbox(self):
        """Fixture for an empty chatbox"""
        return ChatMessage('Admin', '      ')

    @pytest.fixture
    def trimmed_chatbox(self):
        """Fixture for a trimmed chatbox"""
        return ChatMessage('Admin', '      Hello world!     ')

    def test_valid_check_string(self, valid_chatbox):
        """
        Test valid check string
        """
        assert build_mock_reply(valid_chatbox) == "Mock reply to: Hello world!"

    def test_empty_message_raise_error(self, empty_chatbox):
        """
        Test empty message raise error
        """
        with pytest.raises(InvalidMessageError):
            build_mock_reply(empty_chatbox)

    def test_trim_value_string(self, trimmed_chatbox):
        """
        Test trim value string
        """
        assert build_mock_reply(trimmed_chatbox) == "Mock reply to: Hello world!"