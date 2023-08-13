"""LLMChatOrchestrator

TODO...
"""

from typing import Any, Callable, Dict, List, Union
from declarai.memory.base import BaseChatMessageHistory
from declarai.memory import InMemoryMessageHistory
from declarai.middlewares.base import TaskMiddleware
from declarai.operators import LLMParamsType
from declarai.operators.base.types import Message, MessageRole
from declarai.operators.base.types.llm import LLMResponse
from declarai.operators.base.types.operator import BaseOperator
from declarai.python_parser.parser import PythonParser

DEFAULT_CHAT_HISTORY = InMemoryMessageHistory


class LLMChatOrchestrator:
    is_declarai = True

    operator: BaseOperator
    middlewares: List[TaskMiddleware]
    llm_response: LLMResponse
    _kwargs: Dict[str, Any]

    def __init__(
        self,
        decorated: Any,
        operator: Callable[..., BaseOperator],
        middlewares: List[TaskMiddleware] = None,
        llm_params: LLMParamsType = None,
        chat_history: BaseChatMessageHistory = None,
        **kwargs
    ):
        self.parsed = PythonParser(decorated)
        self.parsed_send_func = (
            PythonParser(decorated.send) if getattr(decorated, "send", None) else None
        )
        self.middlewares = middlewares
        self.operator = operator(
            parsed=self.parsed, parsed_func=self.parsed_send_func, **kwargs
        )
        self._chat_history = chat_history or DEFAULT_CHAT_HISTORY()
        self.llm_params = llm_params

        self.system = self.operator.system
        self.greeting = kwargs.pop("greeting", getattr(decorated, "greeting", None))
        self.__set_memory()

    def __set_memory(self):
        if self.greeting:
            self.add_message(message=self.greeting, role=MessageRole.assistant)

    @property
    def conversation(self) -> List[Message]:
        return self._chat_history.history

    def compile(self, **kwargs) -> List[Message]:
        compiled = self.operator.compile(messages=self._chat_history.history, **kwargs)
        return compiled

    def add_message(self, message: str, role: MessageRole) -> None:
        self._chat_history.add_message(Message(message=message, role=role))

    def _exec(self, kwargs) -> LLMResponse:
        self.llm_response = self.operator.predict(**kwargs)
        return self.llm_response

    def _exec_with_message_state(self, kwargs) -> Any:
        raw_response = self._exec(kwargs).response
        self.add_message(raw_response, role=MessageRole.assistant)
        if self.parsed_send_func:
            return self.parsed_send_func.parse(raw_response)
        return raw_response

    def __call__(self, *, messages: List[Message], llm_params: LLMParamsType = None, **kwargs) -> Any:
        kwargs["messages"] = messages
        runtime_llm_params = llm_params or self.llm_params  # order is important! We prioritize runtime params that
        if runtime_llm_params:
            kwargs["llm_params"] = runtime_llm_params
        return self._exec_with_message_state(kwargs)

    def send(self, message: str, llm_params: Union[LLMParamsType, Dict[str, Any]] = None, **kwargs) -> Any:
        self.add_message(message, role=MessageRole.user)
        return self(messages=self._chat_history.history, llm_params=llm_params, **kwargs)
