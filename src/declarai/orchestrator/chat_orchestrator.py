"""LLMChatOrchestrator

TODO...
"""

from typing import Any, List, Dict, Callable

from declarai.middlewares.base import TaskMiddleware
from declarai.operators.base.types import Message, MessageRole
from declarai.operators.base.types.llm import LLMResponse
from declarai.operators.base.types.operator import BaseOperator
from declarai.python_parser.parser import PythonParser


class LLMChatOrchestrator:
    is_declarai = True

    parser: PythonParser
    operator: BaseOperator
    middlewares: List[TaskMiddleware]
    llm_response: LLMResponse
    _kwargs: Dict[str, Any]

    def __init__(
        self,
        decorated: Any,
        operator: Callable[[Any], BaseOperator],
        middlewares: List[TaskMiddleware] = None,
        **kwargs
    ):
        self.parsed = PythonParser(decorated)
        self.parsed_send_func = (
            PythonParser(decorated.send)
            if getattr(decorated, "send", None)
            else None
        )
        self.middlewares = middlewares
        self.operator = operator(
            parsed=self.parsed,
            parsed_func=self.parsed_send_func,
            **kwargs
        )

        self.system = self.operator.system
        self.greeting = kwargs.pop("greeting", getattr(decorated, "greeting", None))
        self._messages = self.__init_messages()

    def __init_messages(self) -> List[Message]:
        messages = []
        if self.greeting:
            messages.append(
                Message(self.greeting, role=MessageRole.assistant)
            )
        return messages

    @property
    def conversation(self) -> List[Message]:
        return self._messages

    def compile(self, **kwargs) -> List[Message]:
        compiled = self.operator.compile(messages=self._messages, **kwargs)
        return compiled

    def add_message(self, message: str, role: MessageRole) -> None:
        self._messages.append(Message(message, role))

    def _exec(self, kwargs) -> LLMResponse:
        self.llm_response = self.operator.predict(**kwargs)
        return self.llm_response

    def _exec_with_message_state(self, kwargs) -> Any:
        raw_response = self._exec(kwargs).response
        self.add_message(raw_response, role=MessageRole.assistant)
        if self.parsed_send_func:
            return self.parsed_send_func.parse(raw_response)
        return raw_response

    def __call__(self, **kwargs) -> Any:
        self._kwargs = kwargs
        return self._exec_with_message_state(kwargs)

    def send(self, **kwargs) -> Any:
        self.add_message(kwargs['message'], role=MessageRole.user)
        return self(messages=self._messages)
