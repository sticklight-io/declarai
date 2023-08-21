"""
The logic for constructing the output prompt.
These methods accept all "return" related properties of the python function and build a string
output prompt from them.
"""
from typing import Optional


def compile_output_schema_template(
    return_name: str, return_type: str, return_doc: str, structured_template: str
) -> str:
    if not any([return_name, return_type, return_doc]):
        return ""
    return_name = return_name or "declarai_result"
    output_schema = f'"{return_name}": '

    if return_type:
        output_schema += str(return_type)

    if return_doc:
        if not return_type and not return_name:
            return f"{return_doc}: "
        output_schema += f"  # {return_doc}"

    if not output_schema:
        return ""

    return structured_template.format(
        output_schema=output_schema, return_name=return_name
    )


def compile_unstructured_template(return_type: str, return_docstring: str) -> str:
    """
    Compiles the output prompt for unstructured output but where still a return type is expected (for example int, float).
    Args:
        return_type: the type of the return value
        return_docstring: the description of the return value

    Returns:

    """
    if return_type == "str":
        return ""
    output_prompt = ""
    if return_type:
        output_prompt += f"respond only with the value of type {return_type}:"
    if return_docstring:
        output_prompt += f"  # {return_docstring}"

    return output_prompt


def compile_output_prompt(
    str_schema: str,
    return_type: str,
    return_docstring: str,
    return_magic: str = None,
    structured: Optional[bool] = True,
    structured_template: Optional[str] = None,
) -> str:
    """
    Compiles the output prompt for given function properties.
    Args:
        str_schema: tbd
        return_type: tbd
        return_docstring: tbd
        return_magic: tbd
        structured: tbd
        structured_template: tbd

    Returns:

    """
    str_schema = str_schema or return_magic

    if not structured:
        return compile_unstructured_template(return_type, return_docstring)

    return compile_output_schema_template(
        str_schema, return_type, return_docstring, structured_template
    )
