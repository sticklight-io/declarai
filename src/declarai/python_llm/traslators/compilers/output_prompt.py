"""
The logic for constructing the output prompt.
These methods accept all "return" related properties of the python function and build a string
output prompt from them.
"""

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


def compile_output_prompt(
    return_name: str,
    return_type: str,
    return_docstring: str,
    return_magic: str = None,
) -> str:
    return_name = return_name or return_magic or "declarai_result"

    output_prompt = compile_output_schema_template(
        return_name, return_type, return_docstring
    )
    instructions = (
        FORMAT_INSTRUCTIONS + JSON_SNIPPET_TEMPLATE.format(format=output_prompt)
    )
    return instructions
