"""
The logic for constructing the output prompt.
These methods accept all "return" related properties of the python function and build a string
output prompt from them.
"""
from typing import Optional

STRUCTURED_SYSTEM_PROMPT = (
    "You are a REST api endpoint. " "You only answer in JSON structures, nothing else."
)

FORMAT_INSTRUCTIONS = (
    "The output should be a markdown code snippet formatted in the following schema, "
    "including the leading and trailing '```json' and '```':\n"
)
JSON_SNIPPET_TEMPLATE = "```json\n{{{{\n    {format}\n}}}}\n```"


def compile_output_schema_template(
    return_name: str, return_type: str, return_doc: str
) -> str:
    if not any([return_name, return_type, return_doc]):
        return ""

    output_schema = f'"{return_name or "declarai_result"}": '

    if return_type:
        output_schema += str(return_type)

    if return_doc:
        if not return_type and not return_name:
            return f"{return_doc}: "
        output_schema += f"  # {return_doc}"

    if not output_schema:
        return ""

    return output_schema


def compile_unstructured_template(
    return_name: str, return_type: str, return_docstring: str
) -> str:
    output_prompt = "respond only with the value "
    # if return_name:
    #     output_prompt += return_name
    if return_type:
        output_prompt += "of type " + return_type + ":"
    else:
        output_prompt += ":"
    if return_docstring:
        output_prompt += f"  # {return_docstring}"

    return output_prompt


def compile_output_prompt(
    str_schema: str,
    return_type: str,
    return_docstring: str,
    return_magic: str = None,
    structured: Optional[bool] = True,
) -> str:
    str_schema = str_schema or return_magic

    if not structured:
        return compile_unstructured_template(str_schema, return_type, return_docstring)

    return compile_output_schema_template(str_schema, return_type, return_docstring)
    # # return output_prompt
    # instructions = FORMAT_INSTRUCTIONS + JSON_SNIPPET_TEMPLATE.format(
    #     format=output_prompt
    # )
    # return instructions
