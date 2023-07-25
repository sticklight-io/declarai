"""ParsedFunction

A class that parses a function and extracts its docstring and signature.
This class is used to expose simple information that will aid the generation of
the llm generated prompt.

usage:

>>> def my_func(a: str, b:int) -> str:
>>>     '''
>>>     This is the method docstring
>>>     :param a: an input string
>>>     :param b: an input integer
>>>     :return magic applied to a and b
>>>     '''
>>>     return magic(a, b)

>>> parsed_func = ParsedFunction(func)
>>> print(parsed_func.name)
>>> 'my_func'
"""

import inspect
import re
from typing import Callable, Dict, Optional

from .method_docstring_parser import parse_method_docstring


class ParsedFunction:
    def __init__(self, func: Callable):
        self.func = func
        self.__doc = inspect.getdoc(func)
        self.__parsed_doc = parse_method_docstring(self.__doc)
        self.__signature = inspect.signature(func)

    @property
    def name(self) -> str:
        return self.func.__name__

    @property
    def func_args(self) -> Dict[str, str]:
        return {
            param.name: param.annotation.__name__
            for param in dict(self.__signature.parameters).values()
        }

    @property
    def return_type(self) -> str:
        return self.__signature.return_annotation

    @property
    def doc(self) -> str:
        return self.__doc

    @property
    def doc_description(self) -> str:
        return self.__parsed_doc["documentation"]

    @property
    def return_doc(self) -> str:
        return self.__parsed_doc["returns"]

    @property
    def doc_params(self) -> Dict[str, str]:
        params = self.__parsed_doc["params"]
        parsed_params = {}
        for param in params:
            name, doc = param.split(":")
            parsed_params[name] = doc
        return parsed_params

    @property
    def return_name(self) -> Optional[str]:
        func_str = inspect.getsource(self.func)
        pattern = r'return magic\((["\'].*?["\']),'  # Matches the first string value in the magic function
        matches = re.findall(pattern, func_str)
        if not matches:
            return None
        return matches[0]
