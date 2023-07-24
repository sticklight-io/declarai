from enum import Enum


class LLMProviders(str, Enum):
    OPENAI = "openai"


class LLMModels(str, Enum):
    GPT_4 = "gpt-4"
    GPT_3P5_TURBO = "gpt-3.5-turbo"
