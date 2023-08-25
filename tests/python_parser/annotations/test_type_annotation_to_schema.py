from typing import Any, Dict, List

import pytest
from pydantic import BaseModel, Field

from declarai.python_parser.type_annotation_to_schema import (
    type_annotation_to_str_schema,
)


class MockSimpleModel(BaseModel):
    name: str
    numbers: List[int]


class MockComplexModelArray(BaseModel):
    name: str
    children: List[MockSimpleModel]


class MockComplexModelDict(BaseModel):
    name: str
    id: str = Field(description="Describe this field")
    children: Dict[str, MockSimpleModel]


@pytest.mark.parametrize(
    "type_, result",
    [
        (str, "str"),
        (int, "int"),
        (float, "float"),
        (bool, "bool"),
        (List[str], "List[string]"),
        (Dict[str, str], "Dict[string, string]"),
        (Dict[str, int], "Dict[string, integer]"),
        (Dict[float, bool], "Dict[number, boolean]"),
        (
            MockSimpleModel,
            '{{\n    "name": "string",\n    "numbers": [\n        "integer"\n    ]\n}}',
        ),
        (List[MockSimpleModel], "List[{{'name': 'string', 'numbers': ['integer']}}]"),
        (
            Dict[str, MockSimpleModel],
            "Dict[string, {{'name': 'string', 'numbers': ['integer']}}]",
        ),
        (
            MockComplexModelArray,
            "{{\n"
            '    "name": "string",\n'
            '    "children": [\n'
            "        {{\n"
            '            "name": "string",\n'
            '            "numbers": [\n'
            '                "integer"\n'
            "            ]\n"
            "        }}\n"
            "    ]\n"
            "}}",
        ),
        (
            MockComplexModelDict,
            "{{\n"
            '    "name": "string",\n'
            '    "id": "string - Describe this field",\n'
            '    "children": {{\n'
            '        "name": "string",\n'
            '        "numbers": [\n'
            '            "integer"\n'
            "        ]\n"
            "    }}\n"
            "}}",
        ),
    ],
)
def test_type_hint_resolver(type_: Any, result: str):
    assert type_annotation_to_str_schema(type_) == result
