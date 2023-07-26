from abc import ABC

from declarai.python_llm.types import FreeFormDoc, Params, Returns


class BaseDocStringParser(ABC):
    @property
    def freeform(self) -> FreeFormDoc:
        raise NotImplementedError()

    @property
    def params(self) -> Params:
        raise NotImplementedError()

    @property
    def returns(self) -> Returns:
        raise NotImplementedError()
