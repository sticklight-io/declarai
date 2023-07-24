from pydantic import BaseSettings


class OpenAIConfig(BaseSettings):
    USE_AI_OPENAI_TOKEN: str
