from functools import partial

from declarai.api.base_decorator import LLMOrchestratorDecorator
from declarai.operators import resolve_operator
from declarai.orchestrator.chat_orchestrator import LLMChatOrchestrator


class LLMChatDecorator(LLMOrchestratorDecorator):
    def get_operator(self, **kwargs):
        return resolve_operator(
            self.declarai_instance.llm_config, operator_type="chat", **kwargs
        )

    def return_orchestrator(self, decorated_cls):
        def llm_chat_factory(cls, **kwargs):
            llm_chat = LLMChatOrchestrator(
                decorated_cls=decorated_cls,
                operator=self.operator,
                **kwargs,
            )
            llm_chat.__name__ = decorated_cls.__name__
            return llm_chat

        return partial(llm_chat_factory, decorated_cls)
