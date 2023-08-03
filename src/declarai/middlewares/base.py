from abc import abstractmethod
from typing import Any

from declarai.orchestrator.types import LLMTaskOrchestratorType


class TaskMiddleware:
    def __init__(self, task: LLMTaskOrchestratorType, kwargs):
        self._task = task
        self._kwargs = kwargs

    def __call__(self) -> Any:
        self.before(self._task)
        res = self._task._exec(self._kwargs)
        self.after(self._task)
        return res

    @abstractmethod
    def before(self, task: LLMTaskOrchestratorType) -> None:
        pass

    @abstractmethod
    def after(self, task: LLMTaskOrchestratorType) -> None:
        pass
