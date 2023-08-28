"""
Base classes for declarai tasks.
"""
from abc import abstractmethod
from typing import Any, TypeVar

from declarai.operators import BaseChatOperator, BaseOperator, LLMParamsType


class BaseTask:
    """
    Base class for tasks.
    """

    operator: BaseOperator
    "The operator to use for the task"

    @property
    def llm_params(self) -> LLMParamsType:
        """
        Return the LLM parameters that are saved on the operator. These parameters are sent to the LLM when the task is
        executed.
        Returns: The LLM parameters

        """
        return self.operator.llm_params

    @abstractmethod
    def _exec(self, kwargs: dict) -> Any:
        """
        Execute the task
        Args:
            kwargs: the runtime keyword arguments that are used to compile the task prompt.

        Returns: The result of the task, which is the result of the operator.

        """
        pass

    @abstractmethod
    def _exec_middlewares(self, kwargs) -> Any:
        """
        Execute the task middlewares and the task itself
        Args:
            kwargs: the runtime keyword arguments that are used to compile the task prompt.

        Returns: The result of the task, which is the result of the operator. Same as `_exec`.

        """
        pass

    @abstractmethod
    def compile(self, **kwargs) -> str:
        """
        Compile the task to get the prompt sent to the LLM
        Args:
            **kwargs: the runtime keyword arguments that are placed within the prompt string.

        Returns: The prompt string that is sent to the LLM

        """
        pass

    def __call__(self, *args, **kwargs):
        """
        Orchestrates the execution of the task
        Args:
            *args: Depends on the inherited class
            **kwargs: Depends on the inherited class

        Returns: The result of the task, after parsing the result of the llm.

        """
        pass


class BaseChat(BaseTask):
    """
    Base class for chat tasks. Same as `BaseTask`, but with a `BaseChatOperator` instead of a `BaseOperator`.
    See `Chat` for default implementation.
    """

    operator: BaseChatOperator
    "The operator to use for the chat task."


TaskType = TypeVar("TaskType", bound=BaseTask)
