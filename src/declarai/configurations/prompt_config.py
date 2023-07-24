from pydantic import BaseModel


class PromptConfig(BaseModel):
    structured: bool = True
    deterministic: bool = True
    temperature: float | None
    max_tokens: int | None
    top_p: float | None
    frequency_penalty: int | None
    presence_penalty: int | None
