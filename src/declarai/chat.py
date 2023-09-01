"""Chat tasks definition.

Chat tasks are tasks that are meant to be used in an iterative fashion, where the user and the assistant exchange
 messages.

Unlike tasks, chat tasks are storing the message history in a `BaseChatMessageHistory` object, which is used to compile
 the prompt sent to the LLM.

At every iteration, the user message is added to the message history, and the prompt is compiled using the message
 history.
The prompt is then sent to the LLM, and the response is parsed and added to the message history.
"""
from functools import partial
from typing import Any, Callable, Dict, List, Type, Union, overload

from declarai._base import BaseTask
from declarai.memory import InMemoryMessageHistory
from declarai.memory.base import BaseChatMessageHistory
from declarai.middleware.base import TaskMiddleware
from declarai.operators import (
    LLM,
    BaseChatOperator,
    LLMParamsType,
    LLMResponse,
    Message,
    MessageRole,
    resolve_operator,
)
from declarai.operators.utils import format_prompt_msg
from declarai.python_parser.parser import PythonParser
from declarai.task import Task

DEFAULT_CHAT_HISTORY = InMemoryMessageHistory


class ChatMeta(type):
    """
    Metaclass for Chat classes. Used to enable the users to receive the chat instance when using the @chat decorator,
    and still be able to "instantiate" the class.
    """

    _init_args = ()
    _init_kwargs = {}

    def __call__(cls, *args, **kwargs):
        """
        Initialize the Chat instance for the second time, after the decorator has been applied. The parameters are
        the same as the ones used for the decorator, but the ones used for the class initialization are precedence.
        Returns: Chat instance

        """
        # Determine which arguments to use for initialization
        final_args = args if args else cls._init_args
        final_kwargs = {**cls._init_kwargs, **kwargs}

        # Create and initialize the instance
        instance = super().__call__(*final_args, **final_kwargs)

        # Always set the __name__ attribute on the instance
        instance.__name__ = cls.__name__

        return instance


class Chat(BaseTask, metaclass=ChatMeta):
    """
    Chat class used for creating chat tasks.

    Chat tasks are tasks that are meant to be used in an iterative fashion,
    where the user and the assistant exchange messages.

    Attributes:
        is_declarai (bool): A class-level attribute indicating if the chat is of type 'declarai'. Always set to `True`.
        _call_kwargs (Dict[str, Any]): A dictionary to store additional keyword arguments, used for passing kwargs between
         the execution of the chat and the execution of the middlewares.
        middlewares (List[TaskMiddleware] or None): Middlewares used for every iteration of the chat.
        operator (BaseChatOperator): The operator used for the chat.
        conversation (List[Message]): Property that returns a list of messages exchanged in the chat.
         Keep in mind this list does not include the first system message. The system message is stored in the `system`
          attribute.
        _chat_history (BaseChatMessageHistory): The chat history mechanism for the chat.
        greeting (str): The greeting message for the chat.
        system (str): The system message for the chat.

    Args:
        operator (BaseChatOperator): The operator to use for the chat.
        middlewares (List[TaskMiddleware], optional): Middlewares to use for every iteration of the chat. Defaults to
        None.
        chat_history (BaseChatMessageHistory, optional): Chat history mechanism to use. Defaults to
         `DEFAULT_CHAT_HISTORY()`.
        greeting (str, optional): Greeting message to use. Defaults to operator's greeting or None.
        system (str, optional): System message to use. Defaults to operator's system message or None.
        stream (bool, optional): Whether to stream the response from the LLM or not. Defaults to False.
        **kwargs: Additional keyword arguments to pass to the formatting of the system message.
    """

    is_declarai = True
    operator: BaseChatOperator
    _call_kwargs: Dict[str, Any]

    def __init__(
        self,
        *,
        operator: BaseChatOperator,
        middlewares: List[Type[TaskMiddleware]] = None,
        chat_history: BaseChatMessageHistory = None,
        greeting: str = None,
        system: str = None,
        **kwargs,
    ):
        self.middlewares = middlewares
        self.operator = operator
        self._chat_history = chat_history or DEFAULT_CHAT_HISTORY()
        self.greeting = greeting or self.operator.greeting
        self.system = self.__set_system_prompt(system=system, **kwargs)
        self.__set_memory()

    def __set_system_prompt(self, system: str, **kwargs) -> str:
        if system:
            self.operator.system = system
        if kwargs:
            formatted_system = format_prompt_msg(self.operator.system, **kwargs)
            self.operator.system = formatted_system

        return self.operator.system

    def __set_memory(self):
        if self.greeting and len(self._chat_history.history) == 0:
            self.add_message(message=self.greeting, role=MessageRole.assistant)

    @property
    def conversation(self) -> List[Message]:
        """
        Returns:
             a list of messages exchanged in the chat. Keep in mind this list does not include the first system message.
        """
        return self._chat_history.history

    def compile(self, **kwargs) -> List[Message]:
        """
        Compiles a list of messages to be sent to the LLM by the operator.
        This is done by accessing the ._chat_history.history attribute.
        The kwargs that are passed to the compile method are onlu used to populate the system message prompt.
        Args:
            **kwargs: System message prompt kwargs.

        Returns: List[Message] - The compiled messages that will be sent to the LLM.

        """
        messages = kwargs.pop("messages", None) or self._chat_history.history
        compiled = self.operator.compile(messages=messages, **kwargs)
        return compiled

    def add_message(self, message: str, role: MessageRole) -> None:
        """
        Interface to add a message to the chat history.
        Args:
            message (str): The message to add to the chat history.
            role (MessageRole): The role of the message (assistant, user, system, etc.)
        """
        self._chat_history.add_message(Message(message=message, role=role))

    def stream_cleanup(self, last_chunk: LLMResponse) -> None:
        """
        Add the combined response to the database and run any other cleanup logic.
        """
        super().stream_cleanup(last_chunk)
        self.add_message(last_chunk.response, role=MessageRole.assistant)

    def _exec(self, kwargs) -> Any:
        """
        Executes the call to the LLM.

        Args:
            kwargs: Keyword arguments to pass to the LLM like `temperature`, `max_tokens`, etc.

        Returns:
             The raw response from the LLM, together with the metadata.
        """
        if self.operator.streaming:
            # Use the stream_handler generator if streaming is enabled
            stream = self.stream_handler(self.operator.predict(**kwargs))
            self.llm_stream_response = stream
            return self.llm_stream_response
        else:
            self.llm_response = self.operator.predict(**kwargs)
            self.add_message(self.llm_response.response, role=MessageRole.assistant)
            if self.operator.parsed_send_func:
                return self.operator.parsed_send_func.parse(self.llm_response.response)
            return self.llm_response.response

    def _exec_middlewares(self, kwargs) -> Any:
        if self.middlewares:
            exec_with_middlewares = None
            for middleware in self.middlewares:
                exec_with_middlewares = middleware(self, self._call_kwargs)
            if exec_with_middlewares:
                return exec_with_middlewares()
        return self._exec(kwargs)

    def __call__(
        self, *, messages: List[Message], llm_params: LLMParamsType = None
    ) -> Any:
        """
        Executes the call to the LLM, based on the messages passed as argument, and the llm_params.
        The llm_params are passed as a dictionary, and they are used to override the default llm_params of the operator.
        The llm_params also have priority over the params that were used to initialize the chat within the decorator.
        Args:
            messages: The messages to pass to the LLM.
            llm_params: The llm_params to use for the call to the LLM.

        Returns:
            The parsed response from the LLM.

        """
        runtime_kwargs = dict(messages=messages)
        runtime_llm_params = (
            llm_params or self.llm_params
        )  # order is important! We prioritize runtime params that
        if runtime_llm_params:
            runtime_kwargs["llm_params"] = runtime_llm_params

        self._call_kwargs = runtime_kwargs
        return self._exec_middlewares(runtime_kwargs)

    def send(
        self,
        message: str,
        llm_params: Union[LLMParamsType, Dict[str, Any]] = None,
        **kwargs,
    ) -> Any:
        """
        Interface that allows the user to send a message to the LLM. It takes a raw string as input, and returns
         the raw response from the LLM.
        Args:
            message:
            llm_params:
            **kwargs:

        Returns:
            Final response from the LLM, after parsing.

        """
        self.add_message(message, role=MessageRole.user)
        return self(
            messages=self._chat_history.history, llm_params=llm_params, **kwargs
        )


class ChatDecorator:
    """
    A decorator class for receiving a chat class, fulfilled with the provided parameters, and returning a Chat object.

    This class provides the `chat` method which acts as a decorator to create a Chat object.

    Args:
        llm (LLM): Resolved LLM object.

    Attributes:
        llm (LLM): Resolved LLM object.
    """

    def __init__(self, llm: LLM):
        self.llm = llm

    @staticmethod
    @overload
    def chat(
        cls: Type,
    ) -> Type[Chat]:
        """
        Overload signature for the `chat` decorator when applied directly on a class.
        Example:
            @ChatDecorator.chat
            class MyChat(Chat):
                ...
        """
        ...

    @staticmethod
    @overload
    def chat(
        *,
        middlewares: List[TaskMiddleware] = None,
        llm_params: LLMParamsType = None,
        chat_history: BaseChatMessageHistory = None,
        greeting: str = None,
        system: str = None,
        streaming: bool = None,
        **kwargs,
    ) -> Callable[..., Type[Chat]]:
        """
        Overload signature for the `chat` decorator when applied with keyword arguments.

        Example:
            @ChatDecorator.chat(llm_params={"temperature": 0.5})
        """
        ...

    def chat(
        self,
        cls: Type = None,
        *,
        middlewares: List[TaskMiddleware] = None,
        llm_params: LLMParamsType = None,
        chat_history: BaseChatMessageHistory = None,
        greeting: str = None,
        system: str = None,
        streaming: bool = None,
    ):
        """
        Decorator method that converts a class into a chat task class.

        Args:
            cls (Type, optional): The original class that is being decorated.
            middlewares (List[TaskMiddleware], optional): Middlewares to use for every iteration of the chat.
             Defaults to None.
            llm_params (LLMParamsType, optional): Parameters for the LLM. Defaults to None.
            chat_history (BaseChatMessageHistory, optional): Chat history mechanism to use. Defaults to None.
            greeting (str, optional): Greeting message to use. Defaults to None.
            system (str, optional): System message to use. Defaults to None.
            streaming (bool, optional): Whether to use streaming or not. Defaults to None.

        Returns:
            (Type[Chat]): A new Chat class that inherits from the original class and has chat capabilities.


        Example:
            ```python
             @ChatDecorator.chat(llm_params={"temperature": 0.5})
             class MyChat:
                ...

             @ChatDecorator.chat
             class MyChat:
                ...
            ```

        """
        operator_type = resolve_operator(self.llm, operator_type="chat")

        def wrap(cls) -> Type[Chat]:
            non_private_methods = {
                method_name: method
                for method_name, method in cls.__dict__.items()
                if not method_name.startswith("__") and callable(method)
            }
            if "send" in non_private_methods:
                non_private_methods.pop("send")

            parsed_cls = PythonParser(cls)

            _decorator_kwargs = dict(
                operator=operator_type(
                    llm=self.llm,
                    parsed=parsed_cls,
                    llm_params=llm_params,
                    streaming=streaming,
                ),
                middlewares=middlewares,
                chat_history=chat_history,
                greeting=greeting,
                system=system,
            )

            new_chat: Type[Chat] = type(cls.__name__, (Chat,), {})  # noqa
            new_chat.__name__ = cls.__name__
            new_chat._init_args = ()  # any positional arguments
            new_chat._init_kwargs = _decorator_kwargs
            for method_name, method in non_private_methods.items():
                if isinstance(method, Task):
                    _method = method
                else:
                    _method = partial(method, new_chat)
                setattr(new_chat, method_name, _method)
            return new_chat

        if cls is None:
            return wrap
        return wrap(cls)
