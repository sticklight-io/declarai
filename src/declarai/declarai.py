from typing import Any, Dict, Optional, overload

from .llm import (
    LLMSettings,
    ModelsOpenai,
    ProviderOpenai,
    resolve_llm_from_config,
)
from .task_decorator import LLMTaskDecorator


class Declarai:
    """
    A root interface to declarai.
    This class allows creating tasks and other declarai provided tools.
    """

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
        self.llm_config = LLMSettings(**kwargs)
        self.llm = resolve_llm_from_config(self.llm_config, **kwargs)
        self.task = LLMTaskDecorator(self)

    @staticmethod
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
        functions as to simplify handling of lint rules for llm functions.

        Usage:
        ```
        >>>@declarai.task
        ...def add(a: int, b: int) -> int:
        ...    return magic(a, b)
        """
        pass
