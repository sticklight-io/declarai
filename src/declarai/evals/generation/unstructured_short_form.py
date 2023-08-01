from declarai import Declarai


def unstructured_short_form(title: str) -> str:
    """
    Write a 4 line poem based on the given title
    """
    return Declarai.magic(title=title)


unstructured_short_form_kwargs = {"title": "Using LLMs is fun!"}
