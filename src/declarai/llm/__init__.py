from .base_llm import LLM
from .config import LLMConfig
from .openai_llm import OpenAILLM


def resolve_llm_from_config(llm_config: LLMConfig, **kwargs) -> LLM:
    if llm_config.provider == "openai":
        open_ai_token = kwargs.get("openai_token")
        if open_ai_token:
            return OpenAILLM(open_ai_token)
        return OpenAILLM()
    raise NotImplementedError()
