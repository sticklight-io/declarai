from typing import Any, Callable

from .llm import resolve_llm_from_config, LLMConfig
from .python_parser import ParsedFunction
from .tasks.base_llm_task import BaseLLMTask
from .tasks.func_llm_translator import FunctionLLMTranslator
from .templates import InstructFunctionTemplate


# TODO: Figure out typing
class LLMFunction(Callable[[tuple[Any, ...], dict[str, Any]], Any]):
    _use_ai: bool
    _llm_translator: Callable
    _parsed_function: Callable
    _llm_func: Callable


def init_declarai(llm_config: LLMConfig):
    llm = resolve_llm_from_config(llm_config)

    def task(func: Callable) -> LLMFunction:
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

        template = InstructFunctionTemplate.format(
            input_instructions=llm_translator.parsed_func.doc_description,
            input_placeholder=llm_translator.make_input_placeholder(),
            output_instructions=llm_translator.make_output_prompt(),
        )

        llm_task = BaseLLMTask(template=template, llm=llm)

        def llm_function(*args, **kwargs):
            return llm_task.generate(**kwargs)["result"]

        llm_function._use_ai = True
        llm_function.__name__ = func.__name__

        llm_function.llm_task = llm_task
        llm_function.parsed_function = parsed_function
        llm_function.llm_translator = llm_translator

        return llm_function

    return task


def magic(*args, **kwargs):
    pass
