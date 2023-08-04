from typing import overload, Callable, Any, List, Type
from typing_extensions import Self
from declarai.decorators.base import LLMOrchestratorDecorator
from declarai.middlewares.base import TaskMiddleware
from declarai.operators import resolve_operator
from declarai.orchestrator.task_orchestrator import LLMTaskOrchestrator


class LLMTaskDecorator(LLMOrchestratorDecorator):
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

    def get_operator(self, **kwargs):
        return resolve_operator(self.declarai_instance.llm_config, **kwargs)

    def return_orchestrator(self, func):
        llm_task = LLMTaskOrchestrator(
            func, self.operator, middlewares=self.middlewares
        )
        llm_task.__name__ = func.__name__
        return llm_task
