from typing import Any, Dict, Optional


def magic(
    return_name: Optional[str] = None,
    *,
    task_desc: Optional[str] = None,
    input_desc: Optional[Dict[str, str]] = None,
    output_desc: Optional[str] = None,
    **kwargs
) -> Any:
    """
    This is an empty method used as a potential replacement for using the docstring for passing
    parameters to the LLM builder. It can also serve as a fake use of arguments in the defined
    functions as to simplify handling of lint rules for llms functions.

    Usage:
    ```
    >>>@declarai.task
    ...def add(a: int, b: int) -> int:
    ...    return magic(a, b)
    """
    pass
