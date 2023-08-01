from typing import Union
from typing_extensions import Literal

from .base_llm import LLM
from .openai_llm import OpenAILLM
from .settings import LLMSettings

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


def resolve_llm_from_config(llm_config: LLMSettings, **kwargs) -> LLM:
    if llm_config.provider == "openai":
        open_ai_token = kwargs.get("openai_token")
        model = llm_config.model
        if open_ai_token:
            return OpenAILLM(open_ai_token, model=model)
        return OpenAILLM(model=model)
    raise NotImplementedError()
