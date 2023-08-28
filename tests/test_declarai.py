from unittest.mock import MagicMock, patch

import declarai


@patch("declarai.declarai.resolve_llm")
@patch("declarai.declarai.TaskDecorator")
def test_declarai(mocked_task_decorator, mocked_resolve_llm):
    kwargs = {}
    mocked_resolve_llm.return_value = MagicMock()
    mocked_task_decorator.return_value.task = MagicMock()

    dec = declarai.Declarai(provider="test", model="test", **kwargs)

    assert dec.llm == mocked_resolve_llm.return_value
    assert dec.task == mocked_task_decorator.return_value.task

    # Test experimental apis
    assert dec.experimental


def test_declarai_openai():
    kwargs = {"model": "davinci", "openai_token": "test_token"}
    dec = declarai.openai(**kwargs)
    assert dec.llm.provider == "openai"
    assert dec.llm.model == "davinci"
    assert dec.llm.api_key == "test_token"


def test_declarai_openai_back_compat():
    from declarai import Declarai
    kwargs = {"model": "davinci", "openai_token": "test_token"}
    dec = Declarai.openai(**kwargs)
    assert dec.llm.provider == "openai"
    assert dec.llm.model == "davinci"
    assert dec.llm.api_key == "test_token"


def test_declarai_openai_back_compat2():

    kwargs = {"model": "davinci", "openai_token": "test_token"}
    dec = declarai.openai(**kwargs)
    assert dec.llm.provider == "openai"
    assert dec.llm.model == "davinci"
    assert dec.llm.api_key == "test_token"


def test_declarai_azure_openai():
    kwargs = {
        "deployment_name": "test",
        "azure_openai_key": "123",
        "azure_openai_api_base": "456",
        "api_version": "789",
    }
    dec = declarai.azure_openai(**kwargs)

    assert dec.llm.provider == "azure-openai"
    assert dec.llm.model == "test"
    assert dec.llm.api_key == "123"
    assert dec.llm._kwargs["api_base"] == "456"
    assert dec.llm._kwargs["api_version"] == "789"
