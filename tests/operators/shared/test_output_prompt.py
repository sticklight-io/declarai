import pytest

from declarai.operators.openai_operators.task_operator import compile_output_prompt
from declarai.operators.templates import (
    StructuredOutputInstructionPrompt,
    compile_output_schema_template,
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
    output_schema = compile_output_schema_template(
        return_name, return_type, return_doc, StructuredOutputInstructionPrompt
    )
    replacement_prompt = StructuredOutputInstructionPrompt.format(
        return_name=return_name or "declarai_result", output_schema=""
    )
    assert output_schema.replace(replacement_prompt, "") == result


def test_compile_output_prompt():
    return_name = "return_name"
    return_type = "Dict[str, str]"
    return_docstring = "The returned value from this function"

    compiled_output_prompt = compile_output_prompt(
        return_name,
        return_type,
        return_docstring,
        structured_template=StructuredOutputInstructionPrompt,
    )
    formatted_output = (
        '"return_name": Dict[str, str]  # The returned value from this function'
    )
    replacement_prompt = StructuredOutputInstructionPrompt.format(
        return_name=return_name or "declarai_result", output_schema=""
    )
    assert compiled_output_prompt.replace(replacement_prompt, "") == formatted_output
