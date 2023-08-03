from functools import partial

from declarai.decorators.base import LLMOrchestratorDecorator
from declarai.operators import resolve_operator
from declarai.orchestrator.chat_orchestrator import LLMChatOrchestrator
from declarai.orchestrator.task_orchestrator import LLMTaskOrchestrator


class LLMChatDecorator(LLMOrchestratorDecorator):
    def get_operator(self, **kwargs):
        return resolve_operator(
            self.declarai_instance.llm_config, operator_type="chat", **kwargs
        )

    def return_orchestrator(self, decorated_cls):
        non_private_methods = {
            method_name: method
            for method_name, method in decorated_cls.__dict__.items()
            if not method_name.startswith("__") and callable(method)
        }
        if "send" in non_private_methods:
            non_private_methods.pop("send")

        def llm_chat_factory(cls, **kwargs):
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
