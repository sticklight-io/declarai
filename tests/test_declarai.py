from unittest.mock import MagicMock, patch

from declarai import Declarai


@patch("declarai.declarai.resolve_llm")
@patch("declarai.declarai.TaskDecorator")
def test_declarai(mocked_task_decorator, mocked_resolve_llm):
    kwargs = {}
    mocked_resolve_llm.return_value = MagicMock()
    mocked_task_decorator.return_value.task = MagicMock()

    declarai = Declarai(provider="test",

                        **kwargs)

    assert declarai.llm == mocked_resolve_llm.return_value
    assert declarai.task == mocked_task_decorator.return_value.task

    # Test experimental apis
    assert declarai.experimental


def test_declarai_openai():
    kwargs = {
        "model": "davinci",
        "openai_token": "test_token",
        "stream": True,
    }
    declarai = Declarai.openai(
        **kwargs
    )

    assert declarai.llm.streaming is True
    assert declarai.llm.provider == "openai"
    assert declarai.llm.model == "davinci"
    assert declarai.llm.api_key == "test_token"


def test_declarai_azure_openai():
    kwargs = {
        "deployment_name": "test",
        "azure_openai_key": "123",
        "azure_openai_api_base": "456",
        "api_version": "789",
    }
    declarai = Declarai.azure_openai(
        **kwargs
    )

    assert declarai.llm.provider == "azure-openai"
    assert declarai.llm.model == "test"
    assert declarai.llm.api_key == "123"
    assert declarai.llm._kwargs["api_base"] == "456"
    assert declarai.llm._kwargs["api_version"] == "789"
