from typing import List
from unittest.mock import MagicMock, patch

from declarai import Declarai
from declarai.operators.base.types.message import Message


@patch("declarai.declarai.resolve_llm_from_config")
def test_chat(mock_llm_chat):
    declarai = Declarai(provider="test", model="test")

    @declarai.chat
    class TestChat:
        """
        This is a test chat.
        """

    chat = TestChat()
    assert chat.__name__ == "TestChat"
    assert chat.parsed_function
    assert chat.llm_translator
    assert chat._system_message == Message(
        message="This is a test chat.\n", role="system"
    )
    assert chat.prompt_config.structured is False


@patch("declarai.declarai.resolve_llm_from_config")
def test_chat_with_send_override(mock_llm_chat):
    declarai = Declarai(provider="test", model="test")

    @declarai.chat
    class TestChat:
        """
        This is a test chat.
        """

        def send(self, message: str) -> List[str]:
            """

            :param message:
            :return:
            """

    chat = TestChat()
    assert chat.__name__ == "TestChat"
    assert chat.parsed_function
    assert chat.llm_translator
    assert chat._system_message == Message(
        message="This is a test chat.\nYour respones should be a JSON structure with a single key named 'declarai_result', nothing else. The expected format is: \"declarai_result\": List[string]",
        role="system",
    )
    assert chat.prompt_config.structured is True
