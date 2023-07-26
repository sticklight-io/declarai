from typing import Dict


def parse_method_docstring(docstring: str) -> Dict[str, str | None]:
    """
    Parses a docstring into its components.
    The parser expects 3 components in a docstring:
        1. Documentation - The free form text usually located at the beginning of the docstring
        2. Parameters - A list of paramaters for the documented method
        3. Return value - A defention of the return value of the documented method

    Example:

    >>> docstring = '''
    This is the documentation
    :param param1: This is the first parameter
    :param param2: This is the second parameter
    :return: This is the return value
    '''
    >>> parse_method_docstring(docstring)
    >>> {
    >>>     "documentation": "This is the documentation",
    >>>     "params": [
    >>>         "param1: This is the first parameter",
    >>>         "param2: This is the second parameter"
    >>>         ],
    >>>     "returns": "This is the return value"
    >>>}

    :param docstring: A method docstring
    :return: A key value pair of the parsed docstring
    """
    if not docstring:
        return {"documentation": None, "params": None, "returns": None}

    lines = docstring.strip().split("\n")

    # Initialize empty results
    documentation, params, return_val = None, [], []

    # Initialize current section to documentation
    current_section = "documentation"

    for line in lines:
        stripped_line = line.strip()

        # Check if the line starts with :param or :return
        if stripped_line.startswith(":param"):
            current_section = "params"
            params.append(stripped_line[7:])
        elif stripped_line.startswith(":return"):
            current_section = "return_val"
            return_val.append(stripped_line[8:])
        else:
            # If line doesn't start with :param or :return, it's part of the current section
            if current_section == "documentation":
                if documentation:
                    documentation += (
                        " " + stripped_line
                    )  # append to existing documentation
                else:
                    documentation = stripped_line  # first line of the documentation
            elif current_section == "params":
                # Append to the last parameter
                params[-1] += " " + stripped_line
            elif current_section == "return_val":
                # Append to the return value
                return_val[-1] += " " + stripped_line

    # If no params or return values are found, set to None
    params = params if params else None
    return_val = (
        return_val[0] if return_val else None
    )  # assuming only one return statement

    return {"documentation": documentation, "params": params, "returns": return_val}
