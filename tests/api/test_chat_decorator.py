from unittest.mock import MagicMock, patch

from declarai import Declarai
from declarai.operators.base.types.message import Message, MessageRole


@patch("declarai.api.task_decorator.resolve_operator")
@patch("declarai.api.chat_decorator.resolve_operator")
def test_chat(mock_chat_operator, _):
    mock_chat_operator.return_value = MagicMock()
    operator = mock_chat_operator.return_value.return_value = MagicMock()
    operator.system = Message(message="This is a test chat.\n", role=MessageRole.system)

    declarai = Declarai(provider="test", model="test")

    @declarai.Experimental.chat
    class TestChat:
        """
        This is a test chat.
        """

        greeting = "This is a greeting message"

    chat = TestChat()
    assert chat.__name__ == "TestChat"
    assert chat.greeting == "This is a greeting message"
    assert chat.conversation == [
        Message(message="This is a greeting message", role=MessageRole.assistant)
    ]
    assert chat.system == Message(
        message="This is a test chat.\n", role=MessageRole.system
    )
