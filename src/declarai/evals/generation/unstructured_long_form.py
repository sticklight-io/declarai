from declarai import Declarai


def unstructured_long_form(title: str) -> str:
    """
    Write a poem based on the given title
    The poem should have 4 verses
    """
    return Declarai.magic(title)


unstructured_long_form_kwargs = {"title": "Using LLMs is fun!"}
