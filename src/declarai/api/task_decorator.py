from typing import Type

from declarai.operators.openai_operators.openai_operator import OpenAIOperator
from declarai.orchestrator.orchestrator import Orchestrator


class LLMTaskDecorator:
    def __init__(self, declarai_instance):
        self.declarai_instance = declarai_instance

        # TODO: Operator resolving logic?
        # if self.llms.provider:
        operator = OpenAIOperator
        operator.llm = self.declarai_instance.llm
        self.operator = operator
        self.middlewares = []

    # TODO: Handle middlewares
    def __call__(
        self,
        func=None,
        *,
        middlewares: str = None,
    ):
        # When arguments are passed
        if func is None:
            self.middlewares = middlewares
            return self
        else:
            # When no arguments are passed
            return self._task(func)

    def _task(self, func):
        llm_task = Orchestrator(func, self.operator)
        llm_task.__name__ = func.__name__
        return llm_task
