import pytest

from declarai.python_llm.traslators.compilers.output_prompt import (
    compile_output_prompt,
    compile_output_schema_template,
    STRUCTURED_SYSTEM_PROMPT,
)


@pytest.mark.parametrize(
    "return_name, return_type, return_doc, result",
    [
        ("", "", "", ""),
        ("foo", "", "", '"foo": '),
        ("", "int", "", '"declarai_result": int'),
        ("", "", "the foo", '"declarai_result":   # the foo'),
        ("foo", "int", "", '"foo": int'),
        ("foo", "", "the foo", '"foo":   # the foo'),
        ("", "int", "the foo", '"declarai_result": int  # the foo'),
        ("foo", "int", "the foo", '"foo": int  # the foo'),
    ],
)
def test_output_prompt(
    return_name: str, return_type: str, return_doc: str, result: str
):
    output_schema = compile_output_schema_template(return_name, return_type, return_doc)
    replacement_prompt = STRUCTURED_SYSTEM_PROMPT.format(
        return_name=return_name or "declarai_result", output_schema=""
    )
    assert output_schema.replace(replacement_prompt, "") == result


def test_compile_output_prompt():
    return_name = "return_name"
    return_type = "Dict[str, str]"
    return_docstring = "The returned value from this function"

    compiled_output_prompt = compile_output_prompt(
        return_name, return_type, return_docstring
    )
    formatted_output = (
        '"return_name": Dict[str, str]  # The returned value from this function'
    )
    assert compiled_output_prompt == formatted_output
