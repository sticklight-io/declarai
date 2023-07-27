from typing import Dict, Tuple, TypeVar

ParamName = TypeVar("ParamName", bound=str)
ParamDoc = TypeVar("ParamDoc", bound=str)
TypeName = TypeVar("TypeName", bound=str)
ReturnName = TypeVar("ReturnName", bound=str)

DocstringFreeform = TypeVar("FreeFormDoc", bound=str)
DocstringParams = Dict[ParamName, ParamDoc]
DocstringReturn = Tuple[ReturnName, TypeName]
