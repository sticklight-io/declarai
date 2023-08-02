from typing import Dict, Optional, Tuple, TypeVar

ParamName = TypeVar("ParamName", bound=str)
ParamDoc = TypeVar("ParamDoc", bound=str)
TypeName = TypeVar("TypeName", bound=str)
ReturnName = TypeVar("ReturnName", bound=str)

DocstringFreeform = TypeVar("DocstringFreeform", bound=str)
DocstringParams = Dict[ParamName, ParamDoc]
DocstringReturn = Tuple[ReturnName, TypeName]

ArgName = TypeVar("ArgName", bound=str)
ArgType = TypeVar("ArgType")


AnnotatedType = TypeVar("AnnotatedType")


class SignatureReturn:
    def __init__(
        self,
        name: Optional[str] = None,
        str_schema: Optional[str] = None,
        type_: Optional[AnnotatedType] = None,
    ):
        self.name = name
        self.str_schema = str_schema
        self.type_ = type_
