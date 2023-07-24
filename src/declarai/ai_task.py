from typing import Callable, overload

from .llm import LLMConfig, resolve_llm_from_config
from .llm.provider_model_mapping import (
    AllModels,
    ModelsAI21labs,
    ModelsCohere,
    ModelsGoogle,
    ModelsOpenai,
    ProviderAI21labs,
    ProviderCohere,
    ProviderGoogle,
    ProviderOpenai,
)
from .python_parser import ParsedFunction
from .tasks.base_llm_task import BaseLLMTask, LLMTask
from .tasks.func_llm_translator import FunctionLLMTranslator
from .templates import InstructFunctionTemplate


# Custom function to enforce the relationship between PROVIDER and MODELS
@overload
def init_declarai(provider: ProviderOpenai, model: ModelsOpenai) -> Callable[[Callable], LLMTask]:
    ...


@overload
def init_declarai(provider: ProviderCohere, model: ModelsCohere) -> Callable[[Callable], LLMTask]:
    ...


@overload
def init_declarai(provider: ProviderAI21labs, model: ModelsAI21labs) -> Callable[[Callable], LLMTask]:
    ...


@overload
def init_declarai(provider: ProviderGoogle, model: ModelsGoogle) -> Callable[[Callable], LLMTask]:
    ...


def init_declarai(provider: str, model: AllModels) -> Callable[[Callable], LLMTask]:
    llm_config = LLMConfig(provider=provider, model=model)
    llm = resolve_llm_from_config(llm_config)

    def ai_task(func: Callable) -> LLMTask:
        """
        This is a decorator that reads the provided function and translates it to an AI function.
        The code generates templates and configurations to apply to the call at runtime.

        :param func: The function to translate
        :return: An LLM function

        usage:
        ```
        @task
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
        parsed_function = ParsedFunction(func)
        llm_translator = FunctionLLMTranslator(parsed_function)

        llm_task = BaseLLMTask(
            template=InstructFunctionTemplate,
            template_args={
                "input_instructions": llm_translator.parsed_func.doc_description,
                "input_placeholder": llm_translator.make_input_placeholder(),
                "output_instructions": llm_translator.make_output_prompt(),
            },
            llm=llm
        )
        llm_task.compile()

        llm_task.__name__ = func.__name__

        llm_task.parsed_function = parsed_function
        llm_task.llm_translator = llm_translator

        return llm_task

    return ai_task


def magic(*args, **kwargs):
    pass
