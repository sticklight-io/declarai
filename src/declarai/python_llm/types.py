from typing import Tuple, Dict, TypeVar


ParamName = TypeVar("ParamName", bound=str)
ParamDoc = TypeVar("ParamDoc", bound=str)
TypeName = TypeVar("TypeName", bound=str)
ReturnName = TypeVar("ReturnName", bound=str)

FreeFormDoc = TypeVar("FreeFormDoc", bound=str)
Params = Dict[ParamName, ParamDoc]
Returns = Tuple[ReturnName, TypeName]
