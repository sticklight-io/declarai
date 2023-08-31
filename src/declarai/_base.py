"""
Base classes for declarai tasks.
"""
from abc import abstractmethod
from typing import Any, TypeVar, Iterator

from declarai.operators import (
    BaseOperator,
    LLMParamsType,
    LLMResponse,
)


class BaseTask:
    """
    Base class for tasks.
    """

    operator: BaseOperator
    "The operator to use for the task"

    llm_response: LLMResponse
    "The response from the LLM"

    llm_stream_response: Iterator[LLMResponse] = None
    "The response from the LLM when streaming"

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

    def stream_handler(self, stream: Iterator[LLMResponse]) -> Iterator[LLMResponse]:
        """
        A generator that yields each chunk from the stream and collects them in a buffer.
        After the stream is exhausted, it runs the cleanup logic.
        """
        response_buffer = []
        for chunk in stream:
            response_buffer.append(chunk)
            yield chunk

        # After the stream is exhausted, run the cleanup logic
        self.stream_cleanup(response_buffer[-1])

    def stream_cleanup(self, last_chunk: LLMResponse):
        self.llm_response = last_chunk


TaskType = TypeVar("TaskType", bound=BaseTask)
