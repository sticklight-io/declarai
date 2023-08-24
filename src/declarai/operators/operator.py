"""
Operator is a class that is used to wrap the compilation of prompts and the singular execution of the LLM.
"""
from abc import abstractmethod
from typing import Any, Dict, Optional, TypeVar

from declarai.operators.llm import LLM, LLMParamsType, LLMResponse
from declarai.python_parser.parser import PythonParser

CompiledTemplate = TypeVar("CompiledTemplate")


class BaseOperator:
    """
    Operator is a class that is used to wrap the compilation of prompts and the singular execution of the LLM.
    Args:
        llm: The LLM to use for the operator
        parsed (PythonParser): The parsed object that is used to compile the prompts
        llm_params: The parameters to pass to the LLM
        kwargs: Enables passing of additional parameters to the operator
    Attributes:
        llm (LLM): The LLM to use for the operator
        parsed (PythonParser): The parsed object that is used to compile the prompts
        llm_params (LLMParamsType): The parameters that were passed during initialization of the operator

    Methods:
        compile: Compiles the prompts using the parsed object and returns the compiled prompts
        predict: Executes the LLM with the compiled prompts and the llm_params
        parse_output: Parses the output of the LLM

    """

    def __init__(
        self,
        llm: LLM,
        parsed: PythonParser,
        llm_params: LLMParamsType = None,
        **kwargs: Dict,
    ):
        self.llm = llm
        self.parsed = parsed
        self.llm_params = llm_params or {}

    @abstractmethod
    def compile(self, **kwargs) -> CompiledTemplate:
        """
        An abstract method that compiles the prompts using the parsed object and returns the compiled prompts.
        The implementation of this method should be specific to the operator, and should be implemented in the child class.
        Args:
            **kwargs: Any runtime parameters that are passed to the operator. Used to format the prompts placeholders.

        Returns:
            The compiled prompts that can be directly passed to the `predict` method of the LLM

        """
        ...

    # Should add validate that llm params are valid part of the llm (attach llmparams on base operator?)
    def predict(
        self, *, llm_params: Optional[LLMParamsType] = None, **kwargs: object
    ) -> LLMResponse:
        """
        Executes prediction using the LLM.
        It first compiles the prompts using the `compile` method, and then executes the LLM with the compiled prompts and the llm_params.
        Args:
            llm_params: The parameters that are passed during runtime. If provided, they will override the ones provided during initialization.
            **kwargs: The keyword arguments to pass to the `compile` method. Used to format the prompts placeholders.

        Returns:
            The response from the LLM
        """
        llm_params = llm_params or self.llm_params  # Order is important -
        # provided params during execution should override the ones provided during initialization
        return self.llm.predict(**self.compile(**kwargs), **llm_params)

    def parse_output(self, output: str) -> Any:
        """
        Parses the raw output from the LLM into the desired format that was set in the parsed object.
        Args:
            output: llm string output

        Returns:
            Any parsed output
        """
        return self.parsed.parse(output)


class BaseChatOperator(BaseOperator):
    """
    Base class for chat operators.
    It extends the `BaseOperator` class and adds additional attributes that are used for chat operators.
    See `BaseOperator` for more information.

    Args:
        system: The system message that is used for the chat
        greeting: The greeting message that is used for the chat.
        kwargs: Enables passing all the required parameters for `BaseOperator`

    Attributes:
        system (str): The system message that is used for the chat
        greeting (str): The greeting message that is used for the chat.
        parsed_send_func (PythonParser): The parsed object that is used to compile the send function.
    """

    def __init__(self, system: str, greeting: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        self.system = system or self.parsed.docstring_freeform
        self.greeting = greeting or getattr(self.parsed.decorated, "greeting", None)
        self.parsed_send_func = (
            PythonParser(self.parsed.decorated.send)
            if getattr(self.parsed.decorated, "send", None)
            else None
        )
