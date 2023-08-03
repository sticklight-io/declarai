from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, TypeVar

from declarai.operators.base.types.llm import LLM, LLMResponse
from declarai.python_parser.parser import PythonParser

CompiledTemplate = TypeVar("CompiledTemplate")


class BaseOperator(ABC):
    llm: LLM
    llm_params: Optional[Dict[str, Any]] = {}

    def __init__(self, llm: LLM, parsed: PythonParser, **kwargs):
        self.llm = llm
        self.parsed = parsed
        self.llm_response = None

    @abstractmethod
    def compile(self, **kwargs) -> CompiledTemplate:
        ...

    def predict(self, **kwargs) -> LLMResponse:
        return self.llm.predict(**self.compile(**kwargs), **self.llm_params)
