from typing import List
from unittest.mock import MagicMock, patch

from declarai import Declarai
from declarai.tasks.chat.message import Message


@patch("declarai.task_decorator.LLMTask")
@patch("declarai.declarai.resolve_llm_from_config")
def test_task(mock_llm, mock_llm_task):
    mock_llm_task.return_value = MagicMock()
    mock_llm_task.return_value.return_value = "prediction"
    declarai = Declarai(provider="test", model="test")

    @declarai.task
    def test_task(a: str, b: int) -> str:
        """
        This is a test task
        :param a: this is a string
        :param b: this is an integer
        :return: returns a string
        """
        return declarai.magic("return_name", a=a, b=b)

    assert mock_llm_task.called
    assert test_task.__name__ == "test_task"
    assert test_task.parsed_function
    assert test_task.parsed_function.magic.return_name == "return_name"
    assert test_task.llm_translator

    res = test_task(a="a", b=1)
    assert res == mock_llm_task.return_value.return_value


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
        message='This is a test chat.\nYou are a REST api endpoint.You only answer in JSON structures \nwith a single key named \'declarai_result\', nothing else.\nThe expected format is:\n"declarai_result": List[string]',
        role="system"
    )
    assert chat.prompt_config.structured is True
