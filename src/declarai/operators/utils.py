import jinja2


def can_be_jinja(string: str) -> bool:
    """
    Checks if a string can be compiled using the jinja2 template engine.
    """
    if "{{" in string or "{%" in string or "{#" in string:
        try:
            jinja2.Template(string)
            return True
        except jinja2.exceptions.TemplateSyntaxError:
            return False
    else:
        return False


def format_prompt_msg(_string: str, **kwargs) -> str:
    """
    Formats a string using the jinja2 template engine if possible, otherwise uses the python string format.
    Args:
        _string: The string to format
        **kwargs: The kwargs to pass to the template

    Returns: The formatted string
    """
    if can_be_jinja(_string):
        return jinja2.Template(_string).render(**kwargs)
    else:
        return _string.format(**kwargs)
