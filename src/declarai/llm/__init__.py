from .base_llm import LLM
from .config import LLMConfig
from .openai_llm import OpenAILLM


def resolve_llm_from_config(llm_config: LLMConfig) -> LLM:
    if llm_config.provider == "openai":
        return OpenAILLM()
    raise NotImplementedError()
