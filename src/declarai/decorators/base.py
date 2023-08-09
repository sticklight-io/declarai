from abc import abstractmethod
from typing import Any


class LLMOrchestratorDecorator:
    def __init__(
        self,
        declarai_instance,
        **kwargs,
    ):
        """
         Initializes the LLMOrchestratorDecorator instance.
         :param kwargs: Additional keyword arguments.
         """
        self.declarai_instance = declarai_instance

        self.operator = self.get_operator(**kwargs)

    @abstractmethod
    def get_operator(self, **kwargs):
        ...

    @abstractmethod
    def return_orchestrator(self, decorated: Any) -> Any:
        ...
