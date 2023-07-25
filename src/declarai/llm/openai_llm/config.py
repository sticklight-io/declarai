from pydantic import BaseSettings


class OpenAIConfig(BaseSettings):
    OPENAI_API_KEY: str = ""
