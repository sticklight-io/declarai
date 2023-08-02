import logging
from functools import partial
from typing import Optional, List

from declarai.middlewares.types import TaskMiddleware
from declarai.operators import resolve_operator
from declarai.orchestrator.chat_orchestrator import LLMChatOrchestrator

logger = logging.getLogger("LLMChatDecorator")


class LLMChatDecorator:
    def __init__(
        self,
        declarai_instance,
        middlewares: Optional[List[TaskMiddleware]] = None,
        **kwargs,
    ):
        self.declarai_instance = declarai_instance

        operator = resolve_operator(
            self.declarai_instance.llm_config, operator_type="chat", **kwargs
        )
        self.operator = operator
        self.middlewares = middlewares or []

    # TODO: Handle middlewares
    def __call__(
        self,
        func=None,
        *,
        middlewares: str = None,
    ):
        # When arguments are passed
        if func is None:
            self.middlewares = middlewares
            return self
        else:
            # When no arguments are passed
            return self._chat(func)

    def _chat(self, decorated_cls):
        def llm_chat_factory(cls, **kwargs):
            llm_chat = LLMChatOrchestrator(
                decorated_cls=decorated_cls,
                operator=self.operator,
                **kwargs,
            )
            llm_chat.__name__ = decorated_cls.__name__
            return llm_chat

        return partial(llm_chat_factory, decorated_cls)
