from typing import Optional

from declarai.operators.base.types.llm_params import BaseLLMParams


class OpenAILLMParams(BaseLLMParams):
    """
    OpenAI LLM Params when running execution
    """
    temperature: Optional[float]
    max_tokens: Optional[int]
    top_p: Optional[float]
    frequency_penalty: Optional[int]
    presence_penalty: Optional[int]
