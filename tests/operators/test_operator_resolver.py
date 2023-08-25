import os
from unittest.mock import patch

import pytest

from declarai.operators import LLMSettings, resolve_operator, resolve_llm, AzureOpenAITaskOperator
from declarai.operators.openai_operators import OpenAIError, OpenAITaskOperator


def test_resolve_openai_operator_with_token():
    kwargs = {"openai_token": "test_token"}
    llm = resolve_llm(provider="openai", model="davinci", **kwargs)
    operator = resolve_operator(llm_instance=llm, operator_type="task")
    assert operator == OpenAITaskOperator
    assert llm.model == "davinci"
    assert llm.api_key == kwargs["openai_token"]


@patch(
    "declarai.operators.openai_operators.openai_llm.OPENAI_API_KEY",
    "test_token",
)
def test_resolve_openai_operator_without_token():
    llm = resolve_llm(provider="openai", model="davinci")
    operator = resolve_operator(llm, operator_type="task")
    assert operator == OpenAITaskOperator


def test_resolve_openai_operator_no_token_raises_error():
    with pytest.raises(OpenAIError):
        llm = resolve_llm(provider="openai", model="davinci")
        resolve_operator(llm, operator_type="task")


def test_resolve_azure_operator():
    llm = resolve_llm(
        provider="azure-openai",
        model="test",
        azure_openai_key="123",
        azure_openai_api_base="456",
    )
    operator = resolve_operator(llm, operator_type="task")
    assert operator == AzureOpenAITaskOperator
