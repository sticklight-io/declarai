from typing import List
from unittest.mock import MagicMock, patch

from declarai import Declarai
from declarai.operators import Message, LLMResponse


@patch("declarai.declarai.resolve_llm")
def test_chat(mock_resolve_llm):
    llm = MagicMock()
    llm.provider = "openai"
    llm.streaming = False
    llm.predict.return_value = LLMResponse(
        response='{"declarai_result": ["1", "2"]}'
    )
    mock_resolve_llm.return_value = llm


    declarai = Declarai(provider="openai", model="gpt-3.5-turbo")

    @declarai.experimental.chat
    class MyChat:
        """
        This is a test chat.
        """
        greeting = "This is a greeting message"

        def send(self) -> List[str]:
            ...

    chat = MyChat()
    assert chat.system == "This is a test chat."
    assert chat.greeting == "This is a greeting message"
    assert chat.compile() == dict(messages=[
        Message(
            message="This is a test chat./nYour responses should be a JSON structure with a single key named 'declarai_result', nothing else. The expected format is: \"declarai_result\": List[string]",
            role="system"),
        Message(message="This is a greeting message", role="assistant")
    ])

    assert chat.send("return two string numbers in a list") == ["1", "2"]


@patch("declarai.declarai.resolve_llm")
def test_chat_jinja_system(mock_resolve_llm):
    llm = MagicMock()
    llm.provider = "openai"
    mock_resolve_llm.return_value = llm

    declarai = Declarai(provider="openai", model="gpt-3.5-turbo")

    @declarai.experimental.chat
    class MyJinjaChat:
        """
        This is a test chat about {{ topic }}.
        """

    chat = MyJinjaChat(topic="jinja2")
    chat.system = "This is a test chat about jinja2."
