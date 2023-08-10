"""LLMTaskOrchestrator

Provides the most basic component to interact with an LLM.
LLMs are often interacted with via an API. In order to provide prompts and receive predictions,
we will need to create the following:
- parse the provided python code
- Translate the parsed data into the proper prompt for the LLM
- Send the request to the LLM and parse the output back into python

This class is an orchestrator that calls a parser and operators to perform the above tasks.
while the parser is meant to be shared across cases, as python code has a consistent interface,
the different LLM API providers as well as custom models have different APIs with different expected prompt
structures. For that reason, there are multiple implementations of operators, depending on the required use case.
"""

from typing import Any, Callable, Dict, List

from declarai.middlewares.base import TaskMiddleware
from declarai.operators.base.types.llm import LLMResponse
from declarai.operators.base.types.llm_params import LLMParamsType
from declarai.operators.base.types.operator import BaseOperator
from declarai.orchestrator.future_llm_task import FutureLLMTask
from declarai.python_parser.parser import PythonParser


class LLMTaskOrchestrator:
    is_declarai = True

    parser: PythonParser
    operator: BaseOperator
    middlewares: List[TaskMiddleware]
    llm_response: LLMResponse
    _kwargs: Dict[str, Any]

    def __init__(
        self,
        decorated: Any,
        operator: Callable[[Any], BaseOperator],
        middlewares: List[TaskMiddleware] = None,
        llm_params: LLMParamsType = None,
        **kwargs
    ):
        self.parsed = PythonParser(decorated)
        self.middlewares = middlewares
        self.llm_params = llm_params
        self.operator = operator(parsed=self.parsed, **kwargs)

    def compile(self, **kwargs) -> Any:
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

    def _exec(self, kwargs) -> Any:
        self.llm_response = self.operator.predict(**kwargs)
        return self.parsed.parse(self.llm_response.response)

    def _exec_middlewares(self, kwargs) -> Any:
        if self.middlewares:
            exec_with_middlewares = None
            for middleware in self.middlewares:
                exec_with_middlewares = middleware(self, self._kwargs)
            if exec_with_middlewares:
                return exec_with_middlewares()
        return self._exec(kwargs)

    def __call__(self, *, llm_params: LLMParamsType = None, **kwargs) -> Any:
        self._kwargs = kwargs
        runtime_llm_params = llm_params or self.llm_params  # order is important! We prioritize runtime params that
        # were passed
        if runtime_llm_params:
            self._kwargs["llm_params"] = runtime_llm_params
        return self._exec_middlewares(kwargs)
