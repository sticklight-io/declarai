from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, TypeVar

from declarai.operators.llms import LLM
from declarai.python_parsers.function_parser import PythonParser


CompiledTemplate = TypeVar("CompiledTemplate")


class BaseOperator(ABC):
    llm: LLM
    llm_params: Optional[Dict[str, Any]] = {}

    def __init__(self, parsed: PythonParser):
        self.parsed = parsed

    @property
    def prompt_params(self) -> Optional[Dict[str, Any]]:
        return

    @abstractmethod
    def compile(self, **kwargs) -> CompiledTemplate:
        ...

    def predict(self, **kwargs) -> str:
        llm_response = self.llm.predict(**self.compile(**kwargs), **self.llm_params)
        return llm_response.response
