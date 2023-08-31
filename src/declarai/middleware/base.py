"""
Base class for task middlewares.
"""
from abc import abstractmethod  # pylint: disable=E0611
from typing import Any, Dict, Iterator

from declarai._base import TaskType


class TaskMiddleware:
    """
    Base class for task middlewares. Middlewares are used to wrap a task and perform some actions before and after the task is executed.
    Is mainly used for logging, but can be used for other purposes as well.
    Please see `LoggingMiddleware` for an example of a middleware.
    Args:
        task: The task to wrap
        kwargs: The keyword arguments to pass to the task
    Attributes:
        _task: The task to wrap
        _kwargs: The keyword arguments to pass to the task
    """

    def __init__(self, task: TaskType, kwargs: Dict[str, Any] = None):
        self._task = task
        self._kwargs = kwargs

    def _stream(self) -> Iterator:
        """
        Re-streams the streaming response while adding the after sideeffects execution to the generator
        Returns:

        """
        for chunk in self._task._exec(self._kwargs):
            yield chunk
        self.after(self._task)

    def __call__(self) -> Any:
        """
        Once the middleware is called, it executes the task and returns the result.
        Before it executes the task, it calls the `before` method, and after it executes the task, it calls the `after` method.
        Returns:
            The result of the task
        """
        self.before(self._task)
        # # If the task is streaming, handle it differently
        if self._task.operator.streaming:
            # Yield chunks from the task, then call the after method
            return self._stream()
        else:
            # Non-streaming tasks can be handled as before
            res = self._task._exec(self._kwargs)
            self.after(self._task)
            return res

    @abstractmethod
    def before(self, task: TaskType) -> None:
        """
        Executed before the task is executed. Should be used to perform some actions before the task is executed.
        Args:
            task: the task to execute
        """

    @abstractmethod
    def after(self, task: TaskType) -> None:
        """
        Executed after the task is executed. Should be used to perform some actions after the task is executed.
        Args:
            task: the task to execute
        """
