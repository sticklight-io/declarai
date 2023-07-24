from abc import abstractmethod
from typing import TypeVar


class BaseLLM:
    @abstractmethod
    def predict(self, prompt, *args, **kwargs):
        raise NotImplementedError()


LLM = TypeVar("LLM", bound=BaseLLM)
