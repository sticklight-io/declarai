from pydantic import BaseModel


class LLMConfig(BaseModel):
    provider: str
    model: str
