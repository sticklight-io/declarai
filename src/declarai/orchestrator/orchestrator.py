import logging
from functools import partial
from typing import Any, TypeVar, Type

from declarai.operators.base import Operator
from declarai.operators.openai_operator import OpenAIOperator
from declarai.python_parsers.function_parser import PythonParser

INPUTS_TEMPLATE = "Inputs:\n{inputs}\n"
INPUT_LINE_TEMPLATE = "{param}: {{{param}}}"
NEW_LINE_INPUT_LINE_TEMPLATE = "\n{param}: {{{param}}}"

logger = logging.getLogger("FunctionLLMTranslator")

CompiledTemplate = TypeVar("CompiledTemplate")


class Orchestrator:
    parser: PythonParser

    def __init__(self, code: Any, operator: Type["Operator"]):
        self.parsed = PythonParser(code)
        self.operator = operator(self.parsed)

    def compile(self, **kwargs):
        return self.operator.compile(**kwargs)

    def plan(self, **kwargs):
        return self.operator.compile(**kwargs)

    def __call__(self, **kwargs):
        response = self.operator.predict(**kwargs)
        return self.parsed.parse(response)


def my_task(title: str) -> str:
    """
    Generate a poem on the given title
    :param title: the title of the poem
    :return: the poem
    """


task = Orchestrator(my_task, OpenAIOperator)
print(task.compile())
print(task.compile(title="baking a cake"))
print(task(title="baking a cake"))
