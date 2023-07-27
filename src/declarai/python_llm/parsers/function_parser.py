"""ParsedFunction
An interface to extract different parts of the provided function into python objects.
"""

import inspect
import re
from typing import Callable, Dict, Optional

from ..docstring_parsers.reST import ReSTDocstringParser
from ..types import DocstringFreeform, DocstringParams, DocstringReturn


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
        self.__doc = inspect.getdoc(func)
        self.__parsed_doc = ReSTDocstringParser(self.__doc)
        self.__signature = inspect.signature(func)

    @property
    def name(self) -> str:
        return self.func.__name__

    @property
    def signature_kwargs(self) -> Dict[str, str]:
        return {
            param.name: param.annotation.__name__
            for param in dict(self.__signature.parameters).values()
        }

    @property
    def signature_return_type(self) -> Optional[str]:
        # TODO: This return type handling is shit...
        _return_type = self.__signature.return_annotation
        try:
            if issubclass(_return_type, inspect._empty):
                return None
        except:
            print("bad return type")
        _return_type = str(_return_type).replace("typing.", "")
        return _return_type

    @property
    def docstring(self) -> str:
        return self.__doc

    @property
    def docstring_freeform(self) -> DocstringFreeform:
        return self.__parsed_doc.freeform

    @property
    def docstring_params(self) -> DocstringParams:
        return self.__parsed_doc.params

    @property
    def docstring_return(self) -> DocstringReturn:
        return self.__parsed_doc.returns

    @property
    def magic(self) -> Optional[str]:
        func_str = inspect.getsource(self.func)
        # Matches the first string value in the magic function
        pattern = r'return magic\((["\'].*?["\']),'
        matches = re.findall(pattern, func_str)
        if not matches:
            return None
        return matches[0].strip("'").strip('"')
