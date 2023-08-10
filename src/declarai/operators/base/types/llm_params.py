from typing import TypeVar, TypedDict


class BaseLLMParams(TypedDict):
    # Define any common/generic params here
    pass

LLMParamsType = TypeVar("LLMParamsType", bound=BaseLLMParams)
