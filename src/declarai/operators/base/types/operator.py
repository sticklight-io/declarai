from abc import abstractmethod
from typing import Any, Dict, Optional, TypeVar, Generic

from declarai.operators.base.types.llm import LLM, LLMResponse
from declarai.operators.base.types.llm_params import LLMParamsType
from declarai.python_parser.parser import PythonParser

CompiledTemplate = TypeVar("CompiledTemplate")


class BaseOperator(Generic[LLMParamsType]):
    llm: LLM

    def __init__(self, llm: LLM, parsed: PythonParser, llm_params: Optional[Dict[str, Any]] = None, **kwargs):
        self.llm = llm
        self.parsed = parsed
        self.llm_response = None
        self.llm_params = llm_params or {}

    @abstractmethod
    def compile(self, **kwargs) -> CompiledTemplate:
        ...

    def predict(self, *, llm_params: Optional[LLMParamsType] = None, **kwargs: object) -> LLMResponse:
        llm_params = llm_params or self.llm_params  # Order is important -
        # provided params during execution should override the ones provided during initialization
        return self.llm.predict(**self.compile(**kwargs), **llm_params)
