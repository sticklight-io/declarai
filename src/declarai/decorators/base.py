from abc import abstractmethod
from typing import Any, List, Optional

from declarai.middlewares.base import TaskMiddleware


class LLMOrchestratorDecorator:
    def __init__(
        self,
        declarai_instance,
        middlewares: Optional[List[TaskMiddleware]] = None,
        **kwargs,
    ):
        self.declarai_instance = declarai_instance

        self.operator = self.get_operator(**kwargs)
        self.middlewares = middlewares or []

    @abstractmethod
    def get_operator(self, **kwargs):
        ...

    @abstractmethod
    def return_orchestrator(self, decorated: Any) -> Any:
        ...
