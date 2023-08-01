import logging
from typing import Any, TypeVar, Type

from declarai.operators.base_operator import BaseOperator
from declarai.python_parsers.function_parser import PythonParser

INPUTS_TEMPLATE = "Inputs:\n{inputs}\n"
INPUT_LINE_TEMPLATE = "{param}: {{{param}}}"
NEW_LINE_INPUT_LINE_TEMPLATE = "\n{param}: {{{param}}}"

logger = logging.getLogger("FunctionLLMTranslator")


class Orchestrator:
    is_declarai = True

    parser: PythonParser

    def __init__(self, code: Any, operator: Type["BaseOperator"]):
        self.parsed = PythonParser(code)
        self.operator = operator(self.parsed)

    def compile(self, **kwargs):
        return self.operator.compile(**kwargs)

    def plan(self, **kwargs):
        return self.operator.compile(**kwargs)

    def __call__(self, **kwargs):
        response = self.operator.predict(**kwargs)
        return self.parsed.parse(response)
