"""This is the main entry point for declarai. It is used to decorate the package functionalities and serve as the main interface for the user. """
from typing import Any, Dict, Optional, overload

from declarai.chat import ChatDecorator
from declarai.operators import LLMSettings, ModelsOpenai, ProviderOpenai
from declarai.task import TaskDecorator


def magic(
    return_name: Optional[str] = None,
    *,
    task_desc: Optional[str] = None,
    input_desc: Optional[Dict[str, str]] = None,
    output_desc: Optional[str] = None,
    **kwargs
) -> Any:
    """
    This is an empty method used as a potential replacement for using the docstring for passing
    parameters to the LLM builder. It can also serve as a fake use of arguments in the defined
    functions as to simplify handling of lint rules for llms functions.

    Example:
        ```py
        @declarai.task
        def add(a: int, b: int) -> int:
            return magic(a, b)
        ```
    """
    pass


class Declarai:
    """
    A root interface to declarai.
    This class allows creating tasks and other declarai provided tools.

    There are overloads for the constructor that allow for a more declarative way of creating tasks.
    based on the provider and model.

    Args:
        **kwargs: A set of keyword arguments that are passed to the LLMSettings class.

    Attributes:
        llm_settings (LLMSettings): A settings object that is used to configure the LLM.
        task (Callable): A decorator that is used to create tasks.
        experimental (Any): A namespace for experimental features.
        experimental.chat (Callable): A decorator that is used to create chat operators.

    """

    magic = magic

    # *-------------------------------------------------------------------------- *
    # * Custom overloads to enforce the relationship between PROVIDER and MODELS  *
    # * Additionally supported providers should be exposed via the Declarai class *
    # * here:                                                                     *
    # *-------------------------------------------------------------------------- *
    @overload
    def __init__(
        self,
        provider: ProviderOpenai,
        model: ModelsOpenai,
        version: Optional[str] = None,
        openai_token: Optional[str] = None,
    ):
        ...

    # *-------------------------------------------------------------------------- *
    # * Actual implementation of Declarai                                         *
    # *-------------------------------------------------------------------------- *
    def __init__(self, **kwargs):
        self.llm_settings = LLMSettings(**kwargs)
        self.task = TaskDecorator(self.llm_settings, **kwargs).task

        class Experimental:
            chat = ChatDecorator(self.llm_settings, **kwargs).chat

        self.experimental = Experimental
