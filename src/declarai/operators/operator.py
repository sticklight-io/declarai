"""
Operator is a class that is used to wrap the compilation of prompts and the singular execution of the LLM.
"""
from abc import abstractmethod
from typing import Any, Dict, Optional, TypeVar, Union, Iterator, List
from logging import getLogger
from declarai.operators import Message, MessageRole
from declarai.operators.llm import LLM, LLMParamsType, LLMResponse
from declarai.operators.templates import (
    compile_output_prompt,
    StructuredOutputChatPrompt,
)
from declarai.operators.utils import format_prompt_msg
from declarai.python_parser.parser import PythonParser

CompiledTemplate = TypeVar("CompiledTemplate")

logger = getLogger("Operator")


class BaseOperator:
    """
    Operator is a class that is used to wrap the compilation of prompts and the singular execution of the LLM.
    Args:
        llm: The LLM to use for the operator
        parsed (PythonParser): The parsed object that is used to compile the prompts
        llm_params: The parameters to pass to the LLM
        streaming: Whether to use streaming or not
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
        streaming: bool = None,
        **kwargs: Dict,
    ):
        self.llm = llm
        self.parsed = parsed
        self.llm_params = llm_params or {}
        self._call_streaming = streaming

    @property
    def streaming(self) -> bool:
        """
        Returns whether the operator is streaming or not
        Returns:

        """
        if self._call_streaming is not None:
            return self._call_streaming

        if hasattr(self.llm, "streaming"):
            return self.llm.streaming

        return False

    @abstractmethod
    def compile_template(self) -> CompiledTemplate:
        ...

    def compile(self, **kwargs) -> CompiledTemplate:
        """
        Implements the compile method of the BaseOperator class.
        Args:
            **kwargs:

        Returns:
            Dict[str, List[Message]]: A dictionary containing a list of messages.

        """
        template = self.compile_template()
        if kwargs:
            template[-1].message = format_prompt_msg(
                _string=template[-1].message, **kwargs
            )
        return {"messages": template}

    # Should add validate that llm params are valid part of the llm (attach llmparams on base operator?)
    def predict(
        self, *, llm_params: Optional[LLMParamsType] = None, **kwargs: object
    ) -> Union[LLMResponse, Iterator[LLMResponse]]:
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
        if self.streaming is not None:
            llm_params["stream"] = self.streaming  # streaming should be the last param
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

    def __init__(
        self,
        system: Optional[str] = None,
        greeting: Optional[str] = None,
        parsed: PythonParser = None,
        streaming: bool = None,
        **kwargs,
    ):
        super().__init__(parsed=parsed, streaming=streaming, **kwargs)
        self.system = system or self.parsed.docstring_freeform
        self.greeting = greeting or getattr(self.parsed.decorated, "greeting", None)
        self.parsed_send_func = (
            PythonParser(self.parsed.decorated.send)
            if getattr(self.parsed.decorated, "send", None)
            else None
        )

    def _compile_output_prompt(self, template) -> str:
        if not self.parsed_send_func.has_any_return_defs:
            logger.warning(
                "Couldn't create output schema for function %s."
                "Falling back to unstructured output."
                "Please add at least one of the following: return type, return doc, return name",
                self.parsed_send_func.name,
            )
            return ""

        signature_return = self.parsed_send_func.signature_return
        return_name, return_doc = self.parsed_send_func.docstring_return
        return compile_output_prompt(
            return_type=signature_return.str_schema,
            str_schema=return_name,
            return_docstring=return_doc,
            return_magic=self.parsed_send_func.magic.return_name,
            structured=self.parsed_send_func.has_structured_return_type,
            structured_template=template,
        )

    def compile_template(self) -> Message:
        """
        Compiles the system prompt.
        Returns: The compiled system message
        """
        structured_template = StructuredOutputChatPrompt
        if self.parsed_send_func:
            output_schema = self._compile_output_prompt(structured_template)
        else:
            output_schema = None

        if output_schema:
            compiled_system_prompt = f"{self.system}/n{output_schema}"
        else:
            compiled_system_prompt = self.system
        return Message(message=compiled_system_prompt, role=MessageRole.system)

    def compile(self, messages: List[Message], **kwargs) -> CompiledTemplate:
        system_message = self.compile_template()
        return dict(messages=[system_message] + messages)
