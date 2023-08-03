from abc import abstractmethod
from typing import Any, List, Optional

from declarai.middlewares.base import TaskMiddleware


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

    @abstractmethod
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

    @abstractmethod
    def return_orchestrator(self, decorated: Any) -> Any:
        ...
