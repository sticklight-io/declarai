import pytest

from declarai.python_llm.func_llm_translator import make_output_prompt


@pytest.mark.parametrize(
    "return_name, return_type, return_doc, result",
    [
        ("", "", "", ""),
        ("foo", "", "", '"foo": '),
        ("", "int", "", '"declarai_result": int'),
        ("", "", "the foo", "the foo: "),
        ("foo", "int", "", '"foo": int'),
        ("foo", "", "the foo", '"foo":   # the foo'),
        ("", "int", "the foo", '"declarai_result": int  # the foo'),
        ("foo", "int", "the foo", '"foo": int  # the foo'),
    ],
)
def test_output_prompt(
    return_name: str, return_type: str, return_doc: str, result: str
):
    output_schema = make_output_prompt(return_name, return_type, return_doc)
    assert output_schema == result
