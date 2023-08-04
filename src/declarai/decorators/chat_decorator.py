from functools import partial
from typing import overload, List, Type, Callable, Any
from typing_extensions import Self
from declarai.decorators.base import LLMOrchestratorDecorator
from declarai.middlewares.base import TaskMiddleware
from declarai.operators import resolve_operator
from declarai.orchestrator.chat_orchestrator import LLMChatOrchestrator
from declarai.orchestrator.task_orchestrator import LLMTaskOrchestrator


class LLMChatDecorator(LLMOrchestratorDecorator):

    @overload
    def __call__(self, decorated: None = None, *, middlewares: List[Type[TaskMiddleware]]) -> Self:
        ...

    @overload
    def __call__(self, decorated: Callable[..., Any]) -> Callable[..., LLMChatOrchestrator]:
        ...

    def __call__(
        self,
        decorated=None,
        *,
        middlewares: List[TaskMiddleware] = None
    ):
        # When arguments are passed
        if decorated is None:
            self.middlewares = middlewares
            return self
        else:
            # When no arguments are passed
            return self.return_orchestrator(decorated)

    def get_operator(self, **kwargs):
        return resolve_operator(
            self.declarai_instance.llm_config, operator_type="chat", **kwargs
        )

    def return_orchestrator(self, decorated_cls) -> Callable[..., LLMChatOrchestrator]:
        non_private_methods = {
            method_name: method
            for method_name, method in decorated_cls.__dict__.items()
            if not method_name.startswith("__") and callable(method)
        }
        if "send" in non_private_methods:
            non_private_methods.pop("send")

        def llm_chat_factory(cls, **kwargs) -> LLMChatOrchestrator:
            llm_chat = LLMChatOrchestrator(
                decorated=decorated_cls,
                operator=self.operator,
                **kwargs,
            )
            llm_chat.__name__ = decorated_cls.__name__
            for method_name, method in non_private_methods.items():
                if isinstance(method, LLMTaskOrchestrator):
                    _method = method
                else:
                    _method = partial(method, llm_chat)
                setattr(llm_chat, method_name, _method)
            return llm_chat

        return partial(llm_chat_factory, decorated_cls)
