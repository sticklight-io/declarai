from declarai import Declarai

simple_task_significance_kwargs = {
    "title": "Using LLMs is fun!",
}


def generate_a_poem_no_metadata(title: str):
    """
    Write a 4 line poem based on the given title
    """
    return Declarai.magic(title=title)


def generate_a_poem_only_return_type(title: str) -> str:
    """
    Write a 4 line poem based on the given title
    """
    return Declarai.magic(title=title)


def generate_a_poem_only_return_doc(title: str):
    """
    Write a 4 line poem based on the given title
    :return: The generated poem
    """
    return Declarai.magic(title=title)


def generate_a_poem_only_return_magic(title: str):
    """
    Write a 4 line poem based on the given title
    """
    return Declarai.magic("poem", title=title)


def generate_a_poem_return_type_return_doc(title: str) -> str:
    """
    Write a 4 line poem based on the given title
    :return: The generated poem
    """
    return Declarai.magic(title=title)


def generate_a_poem_return_type_return_magic(title: str) -> str:
    """
    Write a 4 line poem based on the given title
    """
    return Declarai.magic("poem", title=title)


def generate_a_poem_return_doc_return_magic(title: str):
    """
    Write a 4 line poem based on the given title
    :return: The generated poem
    """
    return Declarai.magic("poem", title=title)


def generate_a_poem_return_all(title: str) -> str:
    """
    Write a 4 line poem based on the given title
    :return: The generated poem
    """
    return Declarai.magic("poem", title=title)
