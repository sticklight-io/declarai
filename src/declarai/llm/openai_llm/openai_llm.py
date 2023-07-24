import openai

from ..base_llm import BaseLLM
from .config import OpenAIConfig


class OpenAILLM(BaseLLM):
    def __init__(self, openai_token: str = None):
        self.openai = openai

        if not openai_token:
            config = OpenAIConfig()
            openai_token = config.USE_AI_OPENAI_TOKEN

        self.openai.api_key = openai_token

    def predict(
        self,
        prompt,
        model: str = "gpt-3.5-turbo",
        temperature: float = 0,
        max_tokens: int = 3000,
        top_p: float = 1,
        frequency_penalty: int = 0,
        presence_penalty: int = 0,
    ):
        res = self.openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
        )
        return res["choices"][0]["message"]["content"]
