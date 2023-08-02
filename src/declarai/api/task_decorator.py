from typing import Optional, List

from declarai.middlewares.types import TaskMiddleware
from declarai.operators import resolve_operator
from declarai.orchestrator.task_orchestrator import LLMTaskOrchestrator


class LLMTaskDecorator:
    def __init__(
        self,
        declarai_instance,
        middlewares: Optional[List[TaskMiddleware]] = None,
        **kwargs,
    ):
        self.declarai_instance = declarai_instance

        operator = resolve_operator(self.declarai_instance.llm_config, **kwargs)
        self.operator = operator
        self.middlewares = middlewares or []

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
        llm_task = LLMTaskOrchestrator(func, self.operator)
        llm_task.__name__ = func.__name__
        return llm_task
