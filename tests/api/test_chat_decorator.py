from unittest.mock import MagicMock, patch

from declarai import Declarai
from declarai.operators import Message, MessageRole


@patch("declarai.chat.resolve_operator")
def test_chat(mock_chat_resolve_operator):
    operator_class_mock = MagicMock()
    operator_instance_mock = MagicMock()

    # Set the .system attribute on the instance returned by the operator mock when called
    operator_instance_mock.system = "This is a test chat.\n"
    operator_instance_mock.greeting = "This is a greeting message"
    operator_class_mock.return_value = operator_instance_mock

    llm = MagicMock()
    mock_chat_resolve_operator.return_value = (operator_class_mock, llm)
    declarai = Declarai(provider="test", model="test")

    @declarai.experimental.chat
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
    assert chat.system == "This is a test chat.\n"

    @declarai.experimental.chat
    class OverrideChatParams:
        """
        This is a test chat.
        """

        greeting = "This is a greeting message"


    chat2 = OverrideChatParams(greeting="New Message")

    assert chat2.__name__ == "OverrideChatParams"
    assert chat2.greeting == "New Message"
