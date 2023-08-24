"""
LLM implementation for OpenAI
"""
from typing import List, Optional

import openai

from declarai.operators import BaseLLM, BaseLLMParams, LLMResponse, Message

from .settings import OPENAI_API_KEY, OPENAI_MODEL


class OpenAIError(Exception):
    """Generic OpenAI error class when working with OpenAI provider."""

    pass


class OpenAILLM(BaseLLM):
    """
    OpenAI LLM implementation that uses openai sdk to make predictions.
    Args:
        openai_token: OpenAI API key
        model: OpenAI model name
    Attributes:
        openai (openai): OpenAI SDK
        model (str): OpenAI model name
    """

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
        """
        Predicts the next message using OpenAI
        Args:
            messages: List of messages that are used as context for the prediction
            model: the model to use for the prediction
            temperature: the temperature to use for the prediction
            max_tokens: the maximum number of tokens to use for the prediction
            top_p: the top p to use for the prediction
            frequency_penalty: the frequency penalty to use for the prediction
            presence_penalty: the presence penalty to use for the prediction

        Returns:
            LLMResponse: The response from the LLM

        """
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


class OpenAILLMParams(BaseLLMParams):
    """
    OpenAI LLM Params when running execution

    Attributes:
        temperature: the temperature to use for the prediction
        max_tokens: the maximum number of tokens to use for the prediction
        top_p: the top p to use for the prediction
        frequency_penalty: the frequency penalty to use for the prediction
        presence_penalty: the presence penalty to use for the prediction
    """

    temperature: Optional[float]
    max_tokens: Optional[int]
    top_p: Optional[float]
    frequency_penalty: Optional[int]
    presence_penalty: Optional[int]
