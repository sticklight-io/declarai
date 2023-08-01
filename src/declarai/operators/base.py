from abc import ABC, abstractmethod
from typing import Optional, Dict, Any

from declarai.operators.llm import LLM
from declarai.orchestrator.orchestrator import CompiledTemplate
from declarai.python_parsers.function_parser import PythonParser


class Operator(ABC):
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
