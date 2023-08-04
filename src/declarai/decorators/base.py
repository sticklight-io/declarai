from abc import abstractmethod
from typing import Any, List, Optional, overload, Callable, Self, Type

from declarai.middlewares import TaskMiddlewareType
from declarai.middlewares.base import TaskMiddleware
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

    @abstractmethod
    def get_operator(self, **kwargs):
        ...

    @overload
    def __call__(self, decorated: None = None, *, middlewares: List[Type[TaskMiddleware]]) -> Self:
        ...

    @overload
    def __call__(self, decorated: Callable[..., Any]) -> LLMTaskOrchestrator:
        ...

    def __call__(
        self,
        decorated=None,
        *,
        middlewares: List[TaskMiddleware] = None
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
