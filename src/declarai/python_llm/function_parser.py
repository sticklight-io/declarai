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

from .docstring_parsers.reST import ReSTDocstringParser
from .magic_parser import extract_magic_args, Magic
from .types import FreeFormDoc, Params, Returns


class ParsedFunction:
    def __init__(self, func: Callable):
        self.func = func
        self._doc = inspect.getdoc(func)
        self._parsed_doc = ReSTDocstringParser(self._doc)
        self._signature = inspect.signature(func)

    @property
    def name(self) -> str:
        return self.func.__name__

    @property
    def func_args(self) -> Dict[str, str]:
        return {
            param.name: param.annotation.__name__
            for param in dict(self._signature.parameters).values()
        }

    @property
    def return_type(self) -> Optional[str]:
        _return_type = self._signature.return_annotation
        try:
            if issubclass(_return_type, inspect._empty):
                return None
            return _return_type
        except:
            return _return_type

    @property
    def doc(self) -> str:
        return self._doc

    @property
    def freeform(self) -> FreeFormDoc:
        return self._parsed_doc.freeform

    @property
    def params(self) -> Params:
        params = self._parsed_doc.params
        parsed_params = {}
        for param in params:
            name, doc = param.split(":")
            parsed_params[name] = doc
        return parsed_params

    @property
    def returns(self) -> Returns:
        return self._parsed_doc.returns

    @property
    def magic(self) -> Magic:
        func_str = inspect.getsource(self.func)
        if "magic(" not in func_str:
            return Magic()
        return extract_magic_args(func_str)
