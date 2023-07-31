"""ParsedFunction
An interface to extract different parts of the provided function into python objects.
"""

import inspect
from typing import Callable, Dict, Optional, TypeVar

from ..magic_parser import Magic, extract_magic_args
from ..types import DocstringFreeform, DocstringParams, DocstringReturn
from .docstring_parsers.reST import ReSTDocstringParser
from .type_hint_resolver import resolve_type_hints


T = TypeVar("T")


class SignatureReturn:
    def __init__(
        self,
        name: Optional[str] = None,
        str_schema: Optional[str] = None,
        type_: Optional[T] = None,
    ):
        self.name = name
        self.str_schema = str_schema
        self.type_ = type_


class ParsedFunction:
    """
    A unified interface for accessing function data.
    This class parses python functions and extracts:
     - function signature:
        - function name
        - args + annotations
        - return type annotation
     - Docstrings:
        - freeform text
        - parameters
        - return descriptions
    - usage of `magic` method in the function

    usage:

    >>> def my_func(a: str, b:int) -> str:
    ...     '''
    ...     This is the method docstring
    ...     :param a: an input string
    ...     :param b: an input integer
    ...     :return magic applied to a and b
    ...     '''
    ...     return magic(a, b)
    >>> parsed_func = ParsedFunction(func)
    >>> print(parsed_func.name)
    >>> 'my_func'
    """

    def __init__(self, func: Callable):
        self.func = func
        self._doc = inspect.getdoc(func)
        self._parsed_doc = ReSTDocstringParser(self._doc)
        self._signature = inspect.signature(func)

    @property
    def name(self) -> str:
        return self.func.__name__

    @property
    def signature_kwargs(self) -> Dict[str, str]:
        return {
            param.name: param.annotation
            for param in dict(self._signature.parameters).values()
        }

    @property
    def signature_return(self) -> Optional[SignatureReturn]:
        return_annotation = self._signature.return_annotation
        if return_annotation == inspect._empty:
            return SignatureReturn()
        _return_type = resolve_type_hints(self._signature.return_annotation)
        return SignatureReturn(
            name=self._signature.return_annotation,
            str_schema=_return_type,
            type_=self._signature.return_annotation,
        )

    @property
    def docstring(self) -> str:
        return self._doc

    @property
    def docstring_freeform(self) -> DocstringFreeform:
        return self._parsed_doc.freeform

    @property
    def docstring_params(self) -> DocstringParams:
        return self._parsed_doc.params

    @property
    def docstring_return(self) -> DocstringReturn:
        return self._parsed_doc.returns

    @property
    def magic(self) -> Magic:
        func_str = inspect.getsource(self.func)
        if "magic(" not in func_str:
            return Magic()
        return extract_magic_args(func_str)
