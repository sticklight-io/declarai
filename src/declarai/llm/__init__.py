from .base_llm import LLM
from .config import LLMConfig
from .openai_llm import OpenAILLM
from .providers import LLMProviders


def resolve_llm_from_config(llm_config: LLMConfig) -> LLM:
    if llm_config.provider == LLMProviders.OPENAI:
        return OpenAILLM()
    raise NotImplementedError()
