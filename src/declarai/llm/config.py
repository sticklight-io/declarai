from typing import Literal, overload
from pydantic import BaseModel

# Define the literals
PROVIDER = Literal["openai", "Cohere", "AI21Labs", "google"]


# Custom function to enforce the relationship between PROVIDER and MODELS
@overload
def init_declarai(provider: Literal["openai"], mode: Literal["gpt-3", "gpt-3.5-turbo", "davinci", "curie", "babbage"]): ...


@overload
def init_declarai(provider: Literal["Cohere"], mode: Literal["claude"]): ...


@overload
def init_declarai(provider: Literal["AI21Labs"], mode: Literal["curie", "babbage"]): ...


@overload
def init_declarai(provider: Literal["google"], model: Literal["palm2", "text-bison"]): ...


class LLMConfig(BaseModel):
    provider: str
    model: str
