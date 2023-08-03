"""PythonParser
An interface to extract different parts of the provided python code into a simple metadata object.
"""

import inspect
from functools import lru_cache as memoized
from typing import Any, Dict, Optional

from pydantic import parse_obj_as, parse_raw_as
from pydantic.error_wrappers import ValidationError

from declarai.python_parser.annotations.type_annotation_to_schema import (
    type_annotation_to_str_schema,
)
from declarai.python_parser.magic_parser import Magic, extract_magic_args
from declarai.python_parser.types import (
    ArgName,
    ArgType,
    DocstringFreeform,
    DocstringParams,
    DocstringReturn,
    SignatureReturn,
)

from .docstring_parsers.reST import ReSTDocstringParser


class OutputParsingError(Exception):
    pass


class PythonParser:
    """
    A unified interface for accessing python parsed data.
    """

    is_func: bool
    is_class: bool
    decorated: Any
    name: str
    signature_return_type: Any
    docstring_freeform: DocstringFreeform
    docstring_params: DocstringParams
    docstring_return: DocstringReturn

    def __init__(self, decorated: Any):
        self.is_func = inspect.isfunction(decorated)
        self.is_class = inspect.isclass(decorated)
        self.decorated = decorated

        # Static attributes:
        self.name = self.decorated.__name__

        self._signature = inspect.signature(self.decorated)
        self.signature_return_type = self.signature_return.type_

        docstring = inspect.getdoc(self.decorated)
        self._parsed_docstring = ReSTDocstringParser(docstring or "")
        self.docstring_freeform = self._parsed_docstring.freeform
        self.docstring_params = self._parsed_docstring.params
        self.docstring_return = self._parsed_docstring.returns

    @property
    @memoized(maxsize=1)
    def signature_kwargs(self) -> Dict[ArgName, ArgType]:
        return {
            param.name: param.annotation
            for param in dict(self._signature.parameters).values()
            if param.name != "self"
        }

    @property
    @memoized(maxsize=1)
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
    @memoized(maxsize=1)
    def magic(self) -> Magic:
        func_str = inspect.getsource(self.decorated)
        if "magic(" not in func_str:
            return Magic()
        return extract_magic_args(func_str)

    @property
    @memoized(maxsize=1)
    def return_name(self) -> str:
        return self.magic.return_name or self.docstring_return[0] or "declarai_result"

    @property
    @memoized(maxsize=1)
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

    @property
    @memoized(maxsize=1)
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

        if self.signature_return_type:
            try:
                return parse_obj_as(self.signature_return_type, parsed_result)
            except ValidationError:
                raise OutputParsingError(
                    f"\nFailed parsing result into type:\n"
                    f"{self.signature_return_type}\n"
                    "----------------------------------\n"
                    f"raw_result:\n"
                    f"{raw_result}"
                )
        else:
            return parsed_result
