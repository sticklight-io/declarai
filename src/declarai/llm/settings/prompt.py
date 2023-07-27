from typing import Optional


class PromptSettings:
    def __init__(
        self,
        structured: bool = True,
        return_name: Optional[str] = "declarai_result",
        temperature: Optional[float] = 0.0,
        max_tokens: Optional[int] = 2000,
        top_p: Optional[float] = 1.0,
        frequency_penalty: Optional[int] = 0,
        presence_penalty: Optional[int] = 0,
    ):
        self.structured = structured
        self.return_name = return_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty
