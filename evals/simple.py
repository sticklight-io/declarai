@declarai.task
def get_tables(query: str) -> List[str]:
    """
    Extract the tables used in the given query
    :param query: sql query
    :return: The tables that are used in the query
    """
    return declarai.magic(query)


print(get_tables(query="SELECT * FROM table_1 JOIN table_2"))


@declarai.task
def a_generate_a_poem(title: str):
    """
    Generate a poem based on the given title
    """
    return declarai.magic(title)


print("No return data")
print(a_generate_a_poem(title="The cat in the hat"))


@declarai.task
def b_generate_a_poem(title: str) -> str:
    """
    Generate a poem based on the given title
    """
    return declarai.magic(title)


print("only return type")
print(b_generate_a_poem(title="The cat in the hat"))


@declarai.task
def c_generate_a_poem(title: str):
    """
    Generate a poem based on the given title
    :return: The generated poem
    """
    return declarai.magic(title)


print("only return doc")
print(c_generate_a_poem(title="The cat in the hat"))


@declarai.task
def d_generate_a_poem(title: str):
    """
    Generate a poem based on the given title
    """
    return declarai.magic("poem", title)


print("only return name")
print(d_generate_a_poem(title="The cat in the hat"))


@declarai.task
def f_generate_a_poem(title: str) -> str:
    """
    Generate a poem based on the given title
    :return: The generated poem
    """
    return declarai.magic(title)


print("return doc + return type")
print(f_generate_a_poem(title="The cat in the hat"))


@declarai.task
def g_generate_a_poem(title: str) -> str:
    """
    Generate a poem based on the given title
    """
    return declarai.magic("poem", title)


print("return name + return type")
print(g_generate_a_poem(title="The cat in the hat"))


@declarai.task
def generate_a_poem(title: str):
    """
    Generate a poem based on the given title
    :return: The generated poem
    """
    return declarai.magic("poem", title)


print("return doc + return name")
print(generate_a_poem(title="The cat in the hat"))


@declarai.task
def h_generate_a_poem(title: str) -> str:
    """
    Generate a poem based on the given title
    :return: The generated poem
    """
    return declarai.magic("poem", title)


print("return all")
print(h_generate_a_poem(title="The cat in the hat"))
