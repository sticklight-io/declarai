"""
LLM implementation for OpenAI
"""
from typing import List, Optional, Iterator, Union

from openai.openai_object import OpenAIObject
import openai

from declarai.operators import BaseLLM, BaseLLMParams, LLMResponse, Message
from declarai.operators.registry import register_llm

from .settings import (
    AZURE_API_VERSION,
    AZURE_OPENAI_API_BASE,
    AZURE_OPENAI_KEY,
    DEPLOYMENT_NAME,
    OPENAI_API_KEY,
    OPENAI_MODEL,
)


class OpenAIError(Exception):
    """Generic OpenAI error class when working with OpenAI provider."""

    pass


class BaseOpenAILLM(BaseLLM):
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

    def __init__(
        self,
        api_key: str,
        api_type: str,
        model_name: str,
        headers: dict = None,
        timeout: int = None,
        stream: bool = None,
        request_timeout: int = None,
        **kwargs,
    ):
        self._kwargs = {
            "headers": headers,
            "timeout": timeout,
            "request_timeout": request_timeout,
            **kwargs,
        }
        self.openai = openai
        self.api_key = api_key
        self.api_type = api_type
        self.stream = stream
        self.model = model_name

    @property
    def streaming(self) -> bool:
        """
        Returns whether the LLM is streaming or not
        Returns:
            bool: True if the LLM is streaming, False otherwise
        """
        return self.stream

    def predict(
        self,
        messages: List[Message],
        model: str = None,
        temperature: float = 0,
        max_tokens: int = 3000,
        top_p: float = 1,
        frequency_penalty: int = 0,
        presence_penalty: int = 0,
        stream: bool = None,
    ) -> Union[Iterator[LLMResponse], LLMResponse]:
        """
        Predicts the next message using OpenAI
        Args:
            stream: if to stream the response
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
        if stream is None:
            stream = self.stream
        openai_messages = [{"role": m.role, "content": m.message} for m in messages]
        res = self.openai.ChatCompletion.create(
            model=model or self.model,
            messages=openai_messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            api_key=self.api_key,
            api_type=self.api_type,
            stream=stream,
            **self._kwargs,
        )

        if stream:
            return handle_streaming_response(res)

        else:
            return LLMResponse(
                response=res.choices[0]["message"]["content"],
                model=res.model,
                prompt_tokens=res["usage"]["prompt_tokens"],
                completion_tokens=res["usage"]["completion_tokens"],
                total_tokens=res["usage"]["total_tokens"],
                raw_response=res.to_dict_recursive(),
            )


@register_llm(provider="openai")
class OpenAILLM(BaseOpenAILLM):
    """
    OpenAI LLM implementation that uses openai sdk to make predictions.
    Args:
        openai_token: OpenAI API key
        model: OpenAI model name
        headers: Headers to use for the request
        timeout: Timeout to use for the request
        stream: Stream to use for the request
        request_timeout: Request timeout to use for the request
    """

    def __init__(
        self,
        openai_token: str = None,
        model: str = None,
        headers: dict = None,
        timeout: int = None,
        stream: bool = None,
        request_timeout: int = None,
    ):
        openai_token = openai_token or OPENAI_API_KEY
        model = model or OPENAI_MODEL
        if not openai_token:
            raise OpenAIError(
                "Missing an OpenAI API key"
                "In order to work with OpenAI, you will need to provide an API key"
                "either by setting the DECLARAI_OPENAI_API_KEY or by providing"
                "the API key via the init interface."
            )
        if not model:
            raise OpenAIError(
                "Missing an OpenAI model"
                "In order to work with OpenAI, you will need to provide a model"
                "either by setting the DECLARAI_OPENAI_MODEL or by providing"
                "the model via the init interface."
            )
        super().__init__(
            openai_token, "openai", model, headers, timeout, stream, request_timeout
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


@register_llm(provider="azure-openai")
class AzureOpenAILLM(BaseOpenAILLM):
    """
    Azure OpenAI LLM implementation that uses openai sdk to make predictions with Azure's OpenAI.
    Args:
        azure_openai_key: Azure OpenAI API key
        azure_openai_api_base: Azure OpenAI endpoint
        model: Deployment name for the model in Azure
        api_version: Azure API version
        headers: Headers to use for the request
        timeout: Timeout to use for the request
        stream: Stream to use for the request
        request_timeout: Request timeout to use for the request
    """

    provider = "azure-openai"

    def __init__(
        self,
        azure_openai_key: str,
        azure_openai_api_base: str,
        model: str,
        api_version: str = None,
        headers: dict = None,
        timeout: int = None,
        stream: bool = None,
        request_timeout: int = None,
    ):
        model = model or DEPLOYMENT_NAME
        api_key = azure_openai_key or AZURE_OPENAI_KEY
        api_version = api_version or AZURE_API_VERSION
        api_base = azure_openai_api_base or AZURE_OPENAI_API_BASE

        super().__init__(
            api_key,
            "azure",
            model,
            headers,
            timeout,
            stream,
            request_timeout,
            engine=model,
            api_version=api_version,
            api_base=api_base,
        )


def handle_streaming_response(api_response: OpenAIObject) -> Iterator[LLMResponse]:
    """
    Accumulate chunk deltas into a full response. Returns the full message.
    """
    response = {"role": None, "response": "", "raw_response": ""}

    for r in api_response:  # noqa
        response["raw_response"] = r.to_dict_recursive()

        delta = r.choices[0]["delta"]
        response["model"] = r.model
        if "usage" in r:
            response["prompt_tokens"] = r.usage["prompt_tokens"]
            response["completion_tokens"] = r.usage["completion_tokens"]
            response["total_tokens"] = r.usage["total_tokens"]

        if "role" in delta:
            response["role"] = delta["role"]

        if delta.get("function_call"):
            fn_call = delta.get("function_call")
            if "function_call" not in response["data"]:
                response["data"]["function_call"] = {"name": None, "arguments": ""}
            if "name" in fn_call:
                response["data"]["function_call"]["name"] = fn_call.name
            if "arguments" in fn_call:
                response["data"]["function_call"]["arguments"] += (
                    fn_call.arguments or ""
                )

        if "content" in delta:
            response["response"] += delta.content or ""

        yield LLMResponse(**response)
