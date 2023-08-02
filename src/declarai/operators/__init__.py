from typing import Type, Union

from typing_extensions import Literal

from declarai.operators.base.llm_settings import LLMSettings

from declarai.operators.base.types.operator import BaseOperator
from .openai_operators.operator import OpenAIOperator

# Based on documentation from https://platform.openai.com/docs/models/overview
ProviderOpenai = Literal["openai"]
ModelsOpenai = Literal[
    "gpt-4",
    "gpt-3.5-turbo",
    "text-davinci-003",
    "text-davinci-002",
    "code-davinci-002",
]


AllModels = Union[ModelsOpenai]


def resolve_operator(llm_config: LLMSettings, **kwargs) -> Type[BaseOperator]:
    if llm_config.provider == "openai":
        open_ai_token = kwargs.get("openai_token")
        model = llm_config.model
        if open_ai_token:
            return OpenAIOperator.new_operator(openai_token=open_ai_token, model=model)
        return OpenAIOperator.new_operator(model=model)
    raise NotImplementedError()
