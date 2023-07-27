from .base_llm import LLM
from .openai_llm import OpenAILLM
from .settings import LLMSettings


def resolve_llm_from_config(llm_config: LLMSettings, **kwargs) -> LLM:
    if llm_config.provider == "openai":
        open_ai_token = kwargs.get("openai_token")
        model = llm_config.get_model_name()
        if open_ai_token:
            return OpenAILLM(open_ai_token, model=model)
        return OpenAILLM(model=model)
    raise NotImplementedError()
