from typing import List, Optional, Any

from declarai.middlewares.base import TaskMiddleware
from declarai.operators import resolve_operator
from declarai.orchestrator.task_orchestrator import LLMTaskOrchestrator


class LLMOrchestratorDecorator:
    def __init__(
        self,
        declarai_instance,
        middlewares: Optional[List[TaskMiddleware]] = None,
        **kwargs,
    ):
        self.declarai_instance = declarai_instance

        self.operator = self.get_operator(**kwargs)
        self.middlewares = middlewares or []

    def get_operator(self, **kwargs):
        ...

    def __call__(
        self,
        decorated=None,
        *,
        middlewares: List[TaskMiddleware] = None,
    ):
        # When arguments are passed
        if decorated is None:
            self.middlewares = middlewares
            return self
        else:
            # When no arguments are passed
            return self.return_orchestrator(decorated)

    def return_orchestrator(self, decorated: Any) -> Any:
        ...
