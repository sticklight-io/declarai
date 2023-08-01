import pytest

from declarai.python_parsers.docstring_parsers.reST.parser import (
    ReSTDocstringParser,
)

multiline_docstring = """This is the documentation\nwith multiple lines
:param param1: This is the first parameter
    with additional description
:param param2: This is the second parameter
    with more details
:return: This is the return value\n    with multiple lines
"""


@pytest.mark.parametrize(
    "docstring, freeform, params, returns",
    [
        (
            multiline_docstring,
            "This is the documentation\nwith multiple lines",
            {
                "param1": "This is the first parameter\n    with additional description",
                "param2": "This is the second parameter\n    with more details",
            },
            ("", "This is the return value\n    with multiple lines"),
        ),
    ],
)
def test_reST_docstring_parser(docstring, freeform, params, returns):
    parsed_docstring = ReSTDocstringParser(docstring)
    assert parsed_docstring.freeform == freeform
    for param_name, param_doc in parsed_docstring.params.items():
        assert param_name in params
        assert param_doc == params[param_name]
    assert parsed_docstring.returns == returns
