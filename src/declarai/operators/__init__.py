from typing import Optional, Type, Union, overload

from typing_extensions import Literal, Tuple

from .llm import LLM, BaseLLM, BaseLLMParams, LLMParamsType, LLMResponse, LLMSettings
from .message import Message, MessageRole
from .openai_operators.chat_operator import OpenAIChatOperator
from .openai_operators.openai_llm import OpenAILLM
from .openai_operators.task_operator import OpenAITaskOperator
from .operator import BaseChatOperator, BaseOperator

# Based on documentation from https://platform.openai.com/docs/models/overview
ProviderOpenai = Literal["openai"]
ModelsOpenai = Literal[
    "gpt-4",
    "gpt-3.5-turbo",
    "gpt-3.5-turbo-16k",
    "text-davinci-003",
    "text-davinci-002",
    "code-davinci-002",
]

AllModels = Union[ModelsOpenai]


@overload
def resolve_operator(
    llm_config: LLMSettings, operator_type: Literal["task"], **kwargs
) -> Tuple[Type[BaseOperator], LLM]:
    ...


@overload
def resolve_operator(
    llm_config: LLMSettings, operator_type: Literal["chat"], **kwargs
) -> Tuple[Type[BaseChatOperator], LLM]:
    ...


def resolve_operator(
    llm_settings: LLMSettings, operator_type: Literal["chat", "task"], **kwargs
) -> Tuple[Type[BaseOperator], LLM]:
    """
    Resolves the operator to be used for the given llm_settings

    Args:
        llm_settings: llm settings like provider, model, etc
        operator_type: relevant operator type
        kwargs: api keys, etc

    Returns:
        an operator class object of type BaseOperator
        an llm class object of type LLM

    """
    if llm_settings.provider == "openai":
        open_ai_token = kwargs.get("openai_token")
        model = llm_settings.model
        if open_ai_token:
            llm = OpenAILLM(
                model=model,
                openai_token=open_ai_token,
            )
        else:
            llm = OpenAILLM(model=model)

        if operator_type == "task":
            operator = OpenAITaskOperator
        elif operator_type == "chat":
            operator = OpenAIChatOperator
        else:
            raise NotImplementedError(
                f"Operator type : {operator_type} not implemented"
            )
        return operator, llm
    raise NotImplementedError()
