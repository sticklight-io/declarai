from pydantic import BaseModel

from .providers import LLMModels, LLMProviders


class LLMConfig(BaseModel):
    provider: LLMProviders = LLMProviders.OPENAI
    model: LLMModels = LLMModels.GPT_3P5_TURBO
