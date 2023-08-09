from functools import partial
from typing import overload, Callable, Any, List, Type, Optional, Dict
from typing_extensions import Self
from declarai.decorators.base import LLMOrchestratorDecorator
from declarai.middlewares.base import TaskMiddleware
from declarai.operators import resolve_operator
from declarai.orchestrator.task_orchestrator import LLMTaskOrchestrator


class LLMTaskDecorator(LLMOrchestratorDecorator):
    @overload
    def __call__(
        self,
        decorated: None = None,
        *,
        middlewares: List[TaskMiddleware] = None,
        llm_params: Optional[Dict[str, Any]] = None,
    ) -> Self:
        ...

    @overload
    def __call__(
        self,
        decorated: Callable[..., Any],
        *,
        middlewares: List[TaskMiddleware] = None,
        llm_params: Optional[Dict[str, Any]] = None
    ) -> LLMTaskOrchestrator:
        ...

    def __call__(
        self,
        decorated=None,
        *,
        middlewares: List[TaskMiddleware] = None,
        llm_params: Optional[Dict[str, Any]] = None,
    ):
        """
        Decorates a python function to be a LLMTaskOrchestrator
        :param decorated: the python function
        :param middlewares: the middlewares to use while executing the task
        :param llm_params: the llm params like temperature, top_k, top_p, etc to be used when prompting the task
        """
        # When arguments are passed
        if decorated is None:
            return partial(self.return_orchestrator, middlewares=middlewares, llm_params=llm_params)
        else:
            # When no arguments are passed
            return self.return_orchestrator(decorated)

    def get_operator(self, **kwargs):
        return resolve_operator(self.declarai_instance.llm_config, **kwargs)

    def return_orchestrator(
        self,
        func,
        middlewares: List[TaskMiddleware] = None,
        llm_params: Optional[Dict[str, Any]] = None
    ):
        llm_task = LLMTaskOrchestrator(
            func, self.operator, middlewares=middlewares, llm_params=llm_params
        )
        llm_task.__name__ = func.__name__
        return llm_task
