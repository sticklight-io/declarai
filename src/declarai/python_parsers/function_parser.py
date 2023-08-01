"""ParsedFunction
An interface to extract different parts of the provided function into python objects.
"""

import inspect
from typing import Callable, Dict, Optional, TypeVar, Any

from pydantic import parse_raw_as, parse_obj_as

from declarai.python_parsers.magic_parser import Magic, extract_magic_args
from declarai.python_parsers.types import DocstringFreeform, DocstringParams, DocstringReturn
from .docstring_parsers.reST import ReSTDocstringParser
from declarai.python_parsers.type_hint_resolver import type_annotation_to_str_schema

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


class PythonParser:
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
    >>> parsed_func = PythonParser(func)
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
        string_schema = type_annotation_to_str_schema(self._signature.return_annotation)
        return SignatureReturn(
            name=str(self._signature.return_annotation),
            str_schema=string_schema,
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

    @property
    def return_name(self) -> str:
        return (
            self.magic.return_name
            or self.docstring_return[0]
            or "declarai_result"
        )

    @property
    def return_type(self) -> Any:
        return self.signature_return.type_

    @property
    def has_any_return_defs(self) -> bool:
        """
        A return definition is any of the following:
        - return type annotation
        - return reference in docstring
        - return referenced in magic placeholder  # TODO: Address magic reference as well.
        """
        return any(
            [
                self.docstring_return[0],
                self.docstring_return[1],
                self.signature_return,
            ]
        )
        # return False

    @property
    def has_structured_return_type(self) -> bool:
        """
        Except for the following types, a dedicated output parsing
        behavior is required to return the expected return type of the task.
        """
        return any(
            [
                self.docstring_return[0],
                self.signature_return.name
                not in (
                    None,
                    "<class 'str'>",
                    "<class 'int'>",
                    "<class 'float'>",
                    "<class 'bool'>",
                ),
                ]
        )

    def parse(self, raw_result: str):
        if self.has_structured_return_type:
            parsed_result = parse_raw_as(dict, raw_result)
            root_key = self.return_name or "declarai_result"
            parsed_result = parsed_result[root_key]
        else:
            parsed_result = raw_result

        return parse_obj_as(self.return_type, parsed_result)
