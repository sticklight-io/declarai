"""
This module defines the base classes for the LLM interface.
"""
from __future__ import annotations

from abc import abstractmethod
from typing import Optional, TypedDict, TypeVar

from pydantic.main import BaseModel


class LLMResponse(BaseModel):
    """
    The response from the LLM.

    Attributes:
        response: The raw response from the LLM
        model: The model that was used to generate the response
        prompt_tokens: The number of tokens in the prompt
        completion_tokens: The number of tokens in the completion
        total_tokens: The total number of tokens in the response
    """

    response: str
    model: Optional[str] = None
    prompt_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None
    total_tokens: Optional[int] = None
    role: str = "assistant"
    raw_response: Optional[dict] = None


class BaseLLMParams(TypedDict):
    """
    The base LLM params that are common to all LLMs.
    """

    # Define any common/generic params here
    pass


class LLMSettings:
    """
    The settings for the LLM. Defines the model and version to use.

    Args:
        provider: The provider of the model (openai, cohere, etc.)
        model: The model to use (gpt-4, gpt-3.5-turbo, etc.)
        version: The version of the model to use (optional)
        **_: Any additional params that are specific to the provider that will be ignored.


    Attributes:
        provider (str): The provider of the model (openai, cohere, etc.)
        model: The full model name to use.
        version: The version of the model to use (optional)
    """

    def __init__(
        self,
        provider: str,
        model: str,
        version: Optional[str] = None,
        **_,
    ):
        self.provider = provider
        self._model = model
        self.version = version

    @property
    def model(self, delimiter: Optional[str] = "-", with_version: bool = True) -> str:
        """
        Some model providers allow defining a base model as well as a sub-model.
        Often the base model is an alias to latest model served on that model.
        for example, when sending gpt-3.5-turbo to OpenAI, the actual model will be one of the
        publicly available snapshots or an internally exposed version as described on their website:
        as of 27/07/2023 - https://platform.openai.com/docs/models/continuous-model-upgrades
        | With the release of gpt-3.5-turbo, some of our models are now being continually updated.
        | We also offer static model versions that developers can continue using for at least
        | three months after an updated model has been introduced.

        Another use-case for sub models is using your own fine-tuned models.
        As described in the documentation:
        https://platform.openai.com/docs/guides/fine-tuning/customize-your-model-name

        You will likely build your fine-tuned model names by concatenating the base model name
        with the fine-tuned model name, separated by a hyphen.
        For example
        gpt-3.5-turbo-declarai-text-classification-2023-03
        or
        gpt-3.5-turbo:declarai:text-classification-2023-03

        In any case you can always pass the full model name in the model parameter and leave the
        sub_model parameter empty if you prefer.
        """
        if self.version and with_version:
            return f"{self._model}{delimiter}{self.version}"
        return self._model


class BaseLLM:
    """
    The base LLM class that all LLMs should inherit from.
    """

    provider: str
    model: str

    @abstractmethod
    def predict(self, *args, **kwargs) -> LLMResponse:
        """
        The predict method that all LLMs should implement.
        Args:
            *args:
            **kwargs:

        Returns: llm response object

        """
        raise NotImplementedError()


LLMParamsType = TypeVar("LLMParamsType", bound=BaseLLMParams)
"""Type variable for LLM params"""
LLM = TypeVar("LLM", bound=BaseLLM)
"""Type variable for LLM"""
