from pydantic import BaseSettings


class OpenAIConfig(BaseSettings):
    OPENAI_TOKEN: str
