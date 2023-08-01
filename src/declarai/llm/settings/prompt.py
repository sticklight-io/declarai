from typing import Any, Optional


class PromptSettings:
    def __init__(
        self,
        structured: bool = True,
        multi_results: bool = False,
        return_name: Optional[str] = "declarai_result",
        return_schema: Optional[str] = "",
        return_type: Optional[Any] = None,
        temperature: Optional[float] = 0.0,
        max_tokens: Optional[int] = 2000,
        top_p: Optional[float] = 1.0,
        frequency_penalty: Optional[int] = 0,
        presence_penalty: Optional[int] = 0,
    ):
        self.structured = structured
        self.multi_results = multi_results
        self.return_name = return_name
        self.return_type = return_type
        self.return_schema = return_schema
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty
