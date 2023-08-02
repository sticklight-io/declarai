"""LLMTaskOrchestrator

Provides the most basic component to interact with an LLM.
LLMs are ofter interacted with via an API. In order to provide prompts and receive predictions,
we will need to create the following:
- parse the provided python code
- Translate the parsed data into the proper prompt for the LLM
- Send the request to the LLM and parse the output back into python

This class is an orchestrator that calls a parser and operators to perform the above tasks.
while the parser is meant to be shared across cases, as python code has a consistent interface,
the different LLM API providers as well as custom models have different APIs with different expected prompt
structures. For that reason, there are multiple implementations of operators, depending on the required use case.
"""

import logging
from typing import Any, Type

from declarai.operators.base.types.operator import BaseOperator
from declarai.orchestrator.future_llm_task import FutureLLMTask
from declarai.python_parser.parser import PythonParser

INPUTS_TEMPLATE = "Inputs:\n{inputs}\n"
INPUT_LINE_TEMPLATE = "{param}: {{{param}}}"
NEW_LINE_INPUT_LINE_TEMPLATE = "\n{param}: {{{param}}}"

logger = logging.getLogger("FunctionLLMTranslator")


class LLMTaskOrchestrator:
    is_declarai = True

    parser: PythonParser
    operator: BaseOperator

    # TODO: Implement fields
    # middlewares
    # llm_response

    def __init__(self, code: Any, operator: Type[BaseOperator]):
        self.parsed = PythonParser(code)
        self.operator = operator(self.parsed)

    def compile(self, **kwargs):
        return self.operator.compile(**kwargs)

    def plan(self, **kwargs) -> FutureLLMTask:
        """
        Populates the compiled template with the actual data.
        :param kwargs: the data to populate the template with
        """

        populated_prompt = self.compile(**kwargs)
        return FutureLLMTask(
            self.__call__,
            kwargs=kwargs,
            compiled_template=self.compile(),
            populated_prompt=populated_prompt,
        )

    # TODO: Handle middlewares
    # def _exec(self, populated_prompt: str) -> Any:
    #     if self.middlewares:
    #         for middleware in self.middlewares:
    #             exec_with_middlewares = middleware(self, populated_prompt)
    #         return exec_with_middlewares()
    #     return self._exec_task(populated_prompt)

    def __call__(self, **kwargs) -> Any:
        response = self.operator.predict(**kwargs)
        return self.parsed.parse(response)

        # self.call_kwargs = kwargs
        # populated_prompt = self._plan(**kwargs)
        # return self._exec(populated_prompt)
