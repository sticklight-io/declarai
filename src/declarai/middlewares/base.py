from typing import Any, Callable, Optional

from declarai.tasks.types import LLMTaskType


class TaskMiddleware:
    before: Optional[Callable[[LLMTaskType], Any]] = lambda self, task: task
    after: Optional[Callable[[LLMTaskType], Any]] = lambda self, task: task
    call: Optional[Callable[[LLMTaskType], Any]] = None

    def __init__(self, task: LLMTaskType, populated_prompt: str):
        self._task = task
        self._populated_prompt = populated_prompt

    def __call__(self) -> Any:
        self.before(self._task)
        res = self._task._exec_task(self._populated_prompt)
        self.after(self._task)
        return res
