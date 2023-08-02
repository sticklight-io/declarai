from declarai.api.base import LLMOrchestratorDecorator
from declarai.operators import resolve_operator
from declarai.orchestrator.task_orchestrator import LLMTaskOrchestrator


class LLMTaskDecorator(LLMOrchestratorDecorator):
    def get_operator(self, **kwargs):
        return resolve_operator(self.declarai_instance.llm_config, **kwargs)

    def return_orchestrator(self, func):
        llm_task = LLMTaskOrchestrator(
            func, self.operator, middlewares=self.middlewares
        )
        llm_task.__name__ = func.__name__
        return llm_task
