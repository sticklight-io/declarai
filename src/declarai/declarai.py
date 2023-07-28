from typing import Callable, Dict, Optional, overload

from .llm import (
    LLMSettings,
    ModelsAI21labs,
    ModelsCohere,
    ModelsGoogle,
    ModelsOpenai,
    ProviderAI21labs,
    ProviderCohere,
    ProviderGoogle,
    ProviderOpenai,
    resolve_llm_from_config,
)
from .python_llm import FunctionLLMTranslator, ParsedFunction
from .tasks.llm_task import LLMTask, LLMTaskType


class Declarai:
    """
    A root interface to declarai.
    This class allows creating tasks and other declarai provided tools.
    """

    # *-------------------------------------------------------------------------- *
    # * Custom overloads to enforce the relationship between PROVIDER and MODELS *
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

    @overload
    def __init__(self, provider: ProviderCohere, model: ModelsCohere):
        ...

    @overload
    def __init__(self, provider: ProviderAI21labs, model: ModelsAI21labs):
        ...

    @overload
    def __init__(self, provider: ProviderGoogle, model: ModelsGoogle):
        ...

    # *-------------------------------------------------------------------------- *
    # * Actual implementation of Declarai *
    # *-------------------------------------------------------------------------- *
    def __init__(self, **kwargs):
        self.llm_config = LLMSettings(**kwargs)
        self.llm = resolve_llm_from_config(self.llm_config, **kwargs)

    @property
    def task(self) -> Callable[[Callable], LLMTaskType]:
        """
        This is a decorator that reads the provided function and translates it to an AI function.
        The code generates templates and configurations to apply to the call at runtime.

        :param func: The function to translate
        :return: An LLM function

        usage:
        ```
        declarai = Declarai(provider="openai", model="gpt-3")

        @declarai.task
        def add(a: int, b: int) -> int:
            '''
            Add two numbers
            :param a: The first number
            :param b: The second number
            :return: The sum of the two numbers
            '''
            return magic(a, b)
        ```
        """

        def ai_task(func: Callable) -> LLMTaskType:
            parsed_function = ParsedFunction(func)
            llm_translator = FunctionLLMTranslator(parsed_function)

            llm_task = LLMTask(
                template=llm_translator.template,
                template_kwargs={
                    "input_instructions": llm_translator.parsed_func.docstring_freeform,
                    "input_placeholder": llm_translator.compile_input_placeholder(),
                    "output_instructions": llm_translator.compile_output_prompt(),
                },
                prompt_kwargs={
                    "structured": llm_translator.has_any_return_defs,
                    "return_name": llm_translator.return_name,
                },
                llm=self.llm,
            )

            llm_task.__name__ = func.__name__

            llm_task.parsed_function = parsed_function
            llm_task.llm_translator = llm_translator

            return llm_task

        return ai_task

    @staticmethod
    def magic(
        return_name: Optional[str] = None,
        *,
        task_desc: Optional[str] = None,
        input_desc: Optional[Dict[str, str]] = None,
        output_desc: Optional[str] = None,
        **kwargs
    ):
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
