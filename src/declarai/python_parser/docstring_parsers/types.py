from abc import ABC  # pylint: disable=E0611

from declarai.python_parser.types import (
    DocstringFreeform,
    DocstringParams,
    DocstringReturn,
)


class BaseDocStringParser(ABC):
    """
    Base class for docstring parsers.
    """

    @property
    def freeform(self) -> DocstringFreeform:
        """
        Return the freeform docstring
        """
        raise NotImplementedError()

    @property
    def params(self) -> DocstringParams:
        """
        Return the params/arguments docstring
        """
        raise NotImplementedError()

    @property
    def returns(self) -> DocstringReturn:
        """
        Return the return docstring
        """
        raise NotImplementedError()
