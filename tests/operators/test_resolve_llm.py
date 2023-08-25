import pytest

from declarai.operators.openai_operators import OpenAIError
from declarai.operators import resolve_llm


def test_resolve_openai_operator_no_token_raises_error():
    with pytest.raises(OpenAIError):
        resolve_llm(provider="openai", model="davinci")
