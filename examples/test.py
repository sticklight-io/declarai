from declarai import init_declarai, magic

ai_task = init_declarai(provider="openai", model="gpt-3.5-turbo")


@ai_task
def a_generate_a_poem(title: str):
    """
    Generate a poem based on the given title
    """
    return magic(title)


print(a_generate_a_poem(title="The cat in the hat"))