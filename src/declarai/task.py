from typing import Callable, overload, Optional, Dict

from .llm import (AllModels, LLMSettings, ModelsAI21labs, ModelsCohere,
                  ModelsGoogle, ModelsOpenai, ProviderAI21labs, ProviderCohere,
                  ProviderGoogle, ProviderOpenai, resolve_llm_from_config)
from .python_llm import FunctionLLMTranslator, ParsedFunction
from .tasks.llm_task import LLMTask, LLMTaskType
from .templates import InstructFunctionTemplate


# Custom function to enforce the relationship between PROVIDER and MODELS
@overload
def init_declarai(
    provider: ProviderOpenai, model: ModelsOpenai, openai_token: Optional[str] = None
) -> Callable[[Callable], LLMTaskType]:
    ...


@overload
def init_declarai(
    provider: ProviderCohere, model: ModelsCohere
) -> Callable[[Callable], LLMTaskType]:
    ...


@overload
def init_declarai(
    provider: ProviderAI21labs, model: ModelsAI21labs
) -> Callable[[Callable], LLMTaskType]:
    ...


@overload
def init_declarai(
    provider: ProviderGoogle, model: ModelsGoogle
) -> Callable[[Callable], LLMTaskType]:
    ...


def init_declarai(
    provider: str, model: AllModels, **kwargs
) -> Callable[[Callable], LLMTaskType]:
    llm_config = LLMSettings(provider=provider, model=model)
    llm = resolve_llm_from_config(llm_config, **kwargs)

    def ai_task(func: Callable) -> LLMTaskType:
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

        return_name = (
            parsed_function.magic
            or parsed_function.docstring_return[0]
            or "declarai_result"
        )

        llm_task = LLMTask(
            template=InstructFunctionTemplate,
            template_kwargs={
                "input_instructions": llm_translator.parsed_func.docstring_freeform,
                "input_placeholder": llm_translator.compile_input_placeholder(),
                "output_instructions": llm_translator.compile_output_prompt(),
            },
            prompt_kwargs={
                "structured": llm_translator.has_any_return_defs,
                "return_name": return_name,
            },
            llm=llm,
        )

        llm_task.__name__ = func.__name__

        llm_task.parsed_function = parsed_function
        llm_task.llm_translator = llm_translator

        return llm_task

    return ai_task


def magic(
    return_name: str,
    *,
    task_desc: str,
    input_desc: Dict[str, str],
    output_desc: str,
    **kwargs
):
    pass