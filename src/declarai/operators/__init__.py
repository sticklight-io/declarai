"""
Operators are the main interface that interacts internally with the LLMs.
"""
from typing import Type, Union, overload

from typing_extensions import Literal

from .llm import LLM, BaseLLM, BaseLLMParams, LLMParamsType, LLMResponse, LLMSettings
from .message import Message, MessageRole
from .openai_operators import (
    AzureOpenAIChatOperator,
    AzureOpenAILLM,
    AzureOpenAITaskOperator,
    OpenAIChatOperator,
    OpenAILLM,
    OpenAITaskOperator,
)
from .operator import BaseChatOperator, BaseOperator
from .registry import llm_registry, operator_registry

# Based on documentation from https://platform.openai.com/docs/models/overview
ProviderOpenai = "openai"
ProviderAzureOpenai = "azure-openai"
ModelsOpenai = Literal[
    "gpt-4",
    "gpt-3.5-turbo",
    "gpt-3.5-turbo-16k",
    "text-davinci-003",
    "text-davinci-002",
    "code-davinci-002",
]
"All official OpenAI models"

AllModels = Union[ModelsOpenai]


def resolve_llm(provider: str, model: str = None, **kwargs) -> LLM:
    """
    Resolves an LLM instance based on the provider and model name.

    Args:
        provider: Name of the provider
        model: Name of the model
        **kwargs: Additional arguments to pass to the LLM initialization

    Returns:
        llm (LLM): instance
    """
    if provider == ProviderOpenai:
        model = LLMSettings(
            provider=provider,
            model=model,
            version=kwargs.pop("version", None),
            **kwargs,
        ).model

    llm_instance = llm_registry.resolve(provider, model, **kwargs)
    return llm_instance


@overload
def resolve_operator(
    llm_instance: LLM, operator_type: Literal["task"]
) -> Type[BaseOperator]:
    ...


@overload
def resolve_operator(
    llm_instance: LLM, operator_type: Literal["chat"]
) -> Type[BaseChatOperator]:
    ...


def resolve_operator(llm_instance: LLM, operator_type: str):
    """
    Resolves an operator based on the LLM instance and the operator type.

    Args:
        llm_instance: instance of initialized LLM
        operator_type (Type[BaseOperator]): task or chat

    Returns:
        Operator type class

    """
    return operator_registry.resolve(llm_instance, operator_type)
