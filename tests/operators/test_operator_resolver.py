import os
from unittest.mock import patch

import pytest

from declarai.operators import resolve_operator
from declarai.operators.base.llm_settings import LLMSettings
from declarai.operators.openai_operators import OpenAITaskOperator
from declarai.operators.openai_operators.openai_llm.openai_llm import OpenAIError


def test_resolve_openai_operator_with_token():
    kwargs = {"openai_token": "test_token"}
    llm_settings = LLMSettings(provider="openai", model="davinci")
    operator = resolve_operator(llm_settings, **kwargs)
    assert operator.func == OpenAITaskOperator


@patch(
    "declarai.operators.openai_operators.openai_llm.openai_llm.OPENAI_API_KEY",
    "test_token",
)
def test_resolve_openai_operator_without_token():
    llm_settings = LLMSettings(provider="openai", model="davinci")
    operator = resolve_operator(llm_settings)
    assert operator.func == OpenAITaskOperator


def test_resolve_openai_operator_no_token_raises_error():
    with pytest.raises(OpenAIError):
        llm_settings = LLMSettings(provider="openai", model="davinci")
        resolve_operator(llm_settings)
