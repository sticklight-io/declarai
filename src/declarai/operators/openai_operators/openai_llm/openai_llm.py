from typing import List

import openai

from declarai.operators.base.types import Message
from declarai.operators.base.types.llm import BaseLLM, LLMResponse

from .settings import OPENAI_API_KEY, OPENAI_MODEL


class OpenAIError(Exception):
    pass


class OpenAILLM(BaseLLM):
    provider = "openai"

    def __init__(self, openai_token: str = None, model: str = None):
        self.openai = openai
        self.openai.api_key = openai_token or OPENAI_API_KEY
        if not self.openai.api_key:
            raise OpenAIError(
                "Missing an OpenAI API key"
                "In order to work with OpenAI, you will need to provide an API key"
                "either by setting the DECLARAI_OPENAI_API_KEY or by providing"
                "the API key via the init interface."
            )
        self.model = model or OPENAI_MODEL

    def predict(
        self,
        messages: List[Message],
        model: str = None,
        temperature: float = 0,
        max_tokens: int = 3000,
        top_p: float = 1,
        frequency_penalty: int = 0,
        presence_penalty: int = 0,
    ) -> LLMResponse:
        openai_messages = [{"role": m.role, "content": m.message} for m in messages]
        res = self.openai.ChatCompletion.create(
            model=model or self.model,
            messages=openai_messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
        )
        return LLMResponse(
            response=res.choices[0]["message"]["content"],
            model=res.model,
            prompt_tokens=res["usage"]["prompt_tokens"],
            completion_tokens=res["usage"]["completion_tokens"],
            total_tokens=res["usage"]["total_tokens"],
        )
