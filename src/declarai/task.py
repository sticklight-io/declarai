"""Task interface

Provides the most basic component to interact with an LLM.
LLMs are often interacted with via an API. In order to provide prompts and receive predictions,
we will need to create the following:
- parse the provided python code
- Translate the parsed data into the proper prompt for the LLM
- Send the request to the LLM and parse the output back into python

This class is an orchestrator that calls a parser and operators to perform the above tasks.
while the parser is meant to be shared across cases, as python code has a consistent interface,
the different LLM API providers as well as custom models have different APIs with different expected prompt
structures. For that reason, there are multiple implementations of operators, depending on the required use case.
"""

from typing import Any, Callable, Dict, List, Optional, Type, overload, Iterator, Union

from declarai._base import BaseTask
from declarai.middleware.base import TaskMiddleware
from declarai.operators import (
    LLM,
    BaseOperator,
    LLMParamsType,
    resolve_operator,
    LLMResponse,
)
from declarai.python_parser.parser import PythonParser


class FutureTask:
    """
    A FutureTask is a wrapper around the task that is returned from the `plan` method.
    It used to create a lazy execution of the task, and to provide additional information about the task.
    The only functionality that is provided by the FutureTask is the `__call__` method, which executes the task.

    Args:
        exec_func: the function to execute when the future task is called
        kwargs: the kwargs that were passed to the task
        compiled_template: the compiled template that was populated by the task
        populated_prompt: the populated prompt that was populated by the task

    Methods:
        __call__: executes the task
    """

    def __init__(
        self,
        exec_func: Callable[[], Any],
        kwargs: Dict[str, Any],
        compiled_template: str,
        populated_prompt: str,
    ):
        self.exec_func = exec_func
        self.__populated_prompt = populated_prompt
        self.__compiled_template = compiled_template
        self.__kwargs = kwargs

    def __call__(self) -> Any:
        """
        Calls the `exec_func` attribute of the FutureTask
        Returns:
            the response from the `exec_func`
        """
        return self.exec_func()

    @property
    def populated_prompt(self) -> str:
        """
        Returns the populated prompt that was populated by the task
        """
        return self.__populated_prompt

    @property
    def compiled_template(self) -> str:
        """
        Returns the compiled template that was populated by the task
        """
        return self.__compiled_template

    @property
    def task_kwargs(self) -> Dict[str, Any]:
        """
        Returns the kwargs that were passed to the task
        """
        return self.__kwargs


class Task(BaseTask):
    """
    Initializes the Task
    Args:
        operator: the operator to use to interact with the LLM
        middlewares: the middlewares to use while executing the task
        **kwargs:

    Attributes:
        operator: the operator to use to interact with the LLM
        _call_kwargs: the kwargs that were passed to the task are set as attributes on the task and passed to the middlewares
    """

    is_declarai = True
    _call_kwargs: Dict[str, Any]

    def __init__(
        self, operator: BaseOperator, middlewares: List[Type[TaskMiddleware]] = None
    ):
        self.middlewares = middlewares
        self.operator = operator

    def compile(self, **kwargs) -> Any:
        """
        Compiles the prompt to be sent to the LLM. This is the first step in the process of interacting with the LLM.
        Can be used for debugging purposes as well, to see what the prompt will look like before sending it to the LLM.
        Args:
            **kwargs: the data to populate the template with

        Returns:
             the compiled template

        """
        return self.operator.compile(**kwargs)

    def plan(self, **kwargs) -> FutureTask:
        """
        Populates the compiled template with the actual data.
        Args:
            **kwargs: the data to populate the template with
        Returns:
             a FutureTask that can be used to execute the task in a lazy manner
        """

        populated_prompt = self.compile(**kwargs)
        return FutureTask(
            self.__call__,
            kwargs=kwargs,
            compiled_template=self.compile(),
            populated_prompt=populated_prompt,
        )

    def _exec(self, kwargs) -> Any:
        if self.operator.streaming:
            stream = self.stream_handler(self.operator.predict(**kwargs))
            self.llm_stream_response = stream
            return self.llm_stream_response
        else:
            self.llm_response = self.operator.predict(**kwargs)
            return self.operator.parse_output(self.llm_response.response)

    def _exec_middlewares(self, kwargs) -> Any:
        if self.middlewares:
            exec_with_middlewares = None
            for middleware in self.middlewares:
                exec_with_middlewares = middleware(self, self._call_kwargs)
            if exec_with_middlewares:
                return exec_with_middlewares()
        return self._exec(kwargs)

    def __call__(
        self, *, llm_params: LLMParamsType = None, **kwargs
    ) -> Union[Any, Iterator[LLMResponse]]:
        """
        Orchestrates the execution of the task.
        Args:
            llm_params: the params to pass to the LLM. If provided, they will override the params that were passed during initialization
            **kwargs: kwargs that are used to compile the template and populate the prompt.

        Returns: the user defined return type of the task

        """
        runtime_llm_params = (
            llm_params or self.llm_params
        )  # order is important! We prioritize runtime params that
        # were passed
        if runtime_llm_params:
            kwargs["llm_params"] = runtime_llm_params

        self._call_kwargs = kwargs
        return self._exec_middlewares(kwargs)


class TaskDecorator:
    """
    The TaskDecorator is used to create a task. It is used as a decorator on a function that will be used as a task.
    Args:
        llm_settings: the settings that define which LLM to use
        **kwargs: additional llm_settings like open_ai_api_key etc.
    Methods:
        task: the decorator that creates the task
    """

    def __init__(self, llm: LLM):
        self.llm = llm

    @staticmethod
    @overload
    def task(
        func: Callable,
    ) -> Task:
        ...

    @staticmethod
    @overload
    def task(
        *,
        middlewares: List[Type[TaskMiddleware]] = None,
        llm_params: LLMParamsType = None,
        streaming: bool = None,
        **kwargs,
    ) -> Callable[[Callable], Task]:
        ...

    def task(
        self,
        func: Optional[Callable] = None,
        *,
        middlewares: List[Type[TaskMiddleware]] = None,
        llm_params: LLMParamsType = None,
        streaming: bool = None,
    ):
        """
        The decorator that creates the task
        Args:
            func: the function to decorate that represents the task
            middlewares: middleware to use while executing the task
            llm_params: llm_params to use when calling the llm
            streaming: whether to stream the response from the llm or not

        Returns:
            (Task): the task that was created

        """
        operator_type = resolve_operator(self.llm, operator_type="task")

        def wrap(_func: Callable) -> Task:
            operator = operator_type(
                parsed=PythonParser(_func),
                llm=self.llm,
                llm_params=llm_params,
                streaming=streaming,
            )
            llm_task = Task(operator=operator, middlewares=middlewares)
            llm_task.__name__ = _func.__name__
            return llm_task

        if func is None:
            return wrap

        return wrap(func)
