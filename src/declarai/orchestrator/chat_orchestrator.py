"""LLMTaskOrchestrator

Provides the most basic component to interact with an LLM.
LLMs are ofter interacted with via an API. In order to provide prompts and receive predictions,
we will need to create the following:
- parse the provided python code
- Translate the parsed data into the proper prompt for the LLM
- Send the request to the LLM and parse the output back into python

This class is an orchestrator that calls a parser and operators to perform the above tasks.
while the parser is meant to be shared across cases, as python code has a consistent interface,
the different LLM API providers as well as custom models have different APIs with different expected prompt
structures. For that reason, there are multiple implementations of operators, depending on the required use case.
"""

import logging
from typing import Any, Type, Optional, List

from declarai.operators.base.types import Message, MessageRole
from declarai.operators.base.types.llm import LLMResponse
from declarai.operators.base.types.operator import BaseOperator
from declarai.python_parser.parser import PythonParser

INPUTS_TEMPLATE = "Inputs:\n{inputs}\n"
INPUT_LINE_TEMPLATE = "{param}: {{{param}}}"
NEW_LINE_INPUT_LINE_TEMPLATE = "\n{param}: {{{param}}}"

logger = logging.getLogger("FunctionLLMTranslator")


class LLMChatOrchestrator:
    is_declarai = True

    parser: PythonParser
    operator: BaseOperator

    def __init__(self,
                 decorated_cls: Any,
                 operator: Type[BaseOperator],
                 **kwargs
                 ):
        self.parsed_decorated_cls = PythonParser(decorated_cls)
        self.parsed_send_func = PythonParser(decorated_cls.send) if getattr(decorated_cls, "send", None) else None
        self.operator = operator(parsed=self.parsed_decorated_cls, parsed_func=self.parsed_send_func, **kwargs)
        self.llm_response: Optional[LLMResponse] = None

        self.greeting = kwargs.pop("greeting", getattr(decorated_cls, "greeting", None))
        self._messages = self.__init_messages()

    @staticmethod
    def format_message(message: str, role: MessageRole) -> Message:
        return Message(message, role=role)

    @property
    def system(self) -> str:
        return self.operator.system

    def __init_messages(self) -> List[Message]:
        messages = []
        if self.greeting:
            messages.append(self.format_message(self.greeting, role=MessageRole.assistant))
        return messages

    @property
    def conversation(self) -> List[Message]:
        return self._messages

    def compile(self, **kwargs) -> List[Message]:
        compiled = self.operator.compile(messages=self._messages, **kwargs)
        return compiled

    def send(self, message: str, **kwargs) -> Any:
        self.add_message(message, role=MessageRole.user)
        return self(**kwargs)

    def add_message(self, message: str, role: MessageRole) -> None:
        self._messages.append(self.format_message(message, role))

    def __call__(self, **kwargs) -> Any:
        messages = self.compile(**kwargs)
        llm_response = self.operator.predict(messages=messages, **kwargs)
        raw_response = llm_response.response
        self.add_message(llm_response.response, role=MessageRole.assistant)
        if self.parsed_send_func:
            return self.parsed_send_func.parse(raw_response)
        return raw_response
