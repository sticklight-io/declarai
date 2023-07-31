from typing_extensions import Literal, Union

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


# Based on documentation from https://docs.cohere.com/reference/generate
ProviderCohere = Literal["Cohere"]
ModelsCohere = Literal[
    "command", "command-nightly", "command-light", "command-light-nightly"
]


ProviderAI21labs = Literal["AI21Labs"]
ModelsAI21labs = Literal["curie", "babbage"]

# Based on documentation from https://cloud.google.com/vertex-ai/docs/generative-ai/learn/models
ProviderGoogle = Literal["google"]
ModelsGoogle = Literal[
    "text-bison",
    "textembedding-gecko",
    "chat-bison",
    "code-bison",
    "codechat-bison",
    "code-gecko",
]

AllModels = Union[ModelsOpenai, ModelsCohere, ModelsAI21labs, ModelsGoogle]


def resolve_llm_from_config(llm_config: LLMSettings, **kwargs) -> LLM:
    if llm_config.provider == "openai":
        open_ai_token = kwargs.get("openai_token")
        model = llm_config.model
        if open_ai_token:
            return OpenAILLM(open_ai_token, model=model)
        return OpenAILLM(model=model)
    raise NotImplementedError()
