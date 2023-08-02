from abc import ABC

from declarai.python_parser.types import (
    DocstringFreeform,
    DocstringParams,
    DocstringReturn,
)


class BaseDocStringParser(ABC):
    @property
    def freeform(self) -> DocstringFreeform:
        raise NotImplementedError()

    @property
    def params(self) -> DocstringParams:
        raise NotImplementedError()

    @property
    def returns(self) -> DocstringReturn:
        raise NotImplementedError()
