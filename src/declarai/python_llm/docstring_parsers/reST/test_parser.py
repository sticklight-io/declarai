import pytest

from declarai.python_llm.docstring_parsers.reST.parser import ReSTDocstringParser


@pytest.mark.parametrize(
    "docstring, freeform, params, returns",
    [
        (
            """This is the documentation\nwith multiple lines\n:param param1: This is the first parameter\n    with additional description\n:param param2: This is the second parameter\n    with more details\n:return: This is the return value\n    with multiple lines""",
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
