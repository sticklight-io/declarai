from typing import Any, Callable, Optional

from declarai.orchestrator.types import LLMTaskOrchestratorType


class TaskMiddleware:
    before: Optional[Callable[[LLMTaskOrchestratorType], Any]] = lambda self, task: task
    after: Optional[Callable[[LLMTaskOrchestratorType], Any]] = lambda self, task: task
    call: Optional[Callable[[LLMTaskOrchestratorType], Any]] = None

    def __init__(self, task: LLMTaskOrchestratorType, kwargs):
        self._task = task
        self._kwargs = kwargs

    def __call__(self) -> Any:
        self.before(self._task)
        res = self._task._exec(self._kwargs)
        self.after(self._task)
        return res
