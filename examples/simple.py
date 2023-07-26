from typing import Dict, List

from declarai import init_declarai, magic

ai_task = init_declarai(provider="openai", model="gpt-3.5-turbo")


@ai_task
def extract_email_phonenum(email: str) -> List[str]:
    """
    Extract the phone number from the provided email
    :param email: email content
    :return: The phone numbers that are used in the email
    """


res = extract_email_phonenum(
    email="Hey jenny,\nyou can call me at 124-3435-132.\n"
    "Thanks!, I'm also available at 123-456-7890."
)

print(extract_email_phonenum.compile())
print(res)

planned = extract_email_phonenum.plan(
    email="Hey jenny,\nyou can call me at 000999999999.\n"
    "Thanks!, I'm also available at 123-456-7890."
)
print(planned.get_populated_prompt())
res_2 = planned()
print(res_2)


@ai_task
def extract_email_info(text: str, contact_fields: List[str]) -> Dict[str, str]:
    """
    Extract the provided contact fields from the given text
    :param text: The text to extract contact information from
    :param contact_fields: The contact fields to extract
    :return: A mapping of the contact fields to their values
    """
    return magic(text, contact_fields)


@ai_task
def extract_email_contacts(text: str, contact_fields: List[str]) -> Dict[str, str]:
    """
    Extract the provided contact fields from the given text
    :param text: The text to extract contact information from
    :param contact_fields: The contact fields to extract
    :return: A mapping of the contact fields to their values
    """
    return magic("contacts", text, contact_fields)


print(
    extract_email_contacts(
        text="I am John Doe and my phone number is 123-456-7890. ",
        contact_fields=["phone", "name", "email"],
    )
)

res = extract_email_info(
    text="I am John Doe and my phone number is 123-456-7890. "
    "My email address is johndoe@walla.co.il",
    contact_fields=["phone", "name", "email"],
)
print(res)


@ai_task
def get_tables(query: str) -> List[str]:
    """
    Extract the tables used in the given query
    :param query: sql query
    :return: The tables that are used in the query
    """
    return magic(query)


print(get_tables(query="SELECT * FROM table_1 JOIN table_2"))


@ai_task
def a_generate_a_poem(title: str):
    """
    Generate a poem based on the given title
    """
    return magic(title)


print("No return data")
print(a_generate_a_poem(title="The cat in the hat"))


@ai_task
def b_generate_a_poem(title: str) -> str:
    """
    Generate a poem based on the given title
    """
    return magic(title)


print("only return type")
print(b_generate_a_poem(title="The cat in the hat"))


@ai_task
def c_generate_a_poem(title: str):
    """
    Generate a poem based on the given title
    :return: The generated poem
    """
    return magic(title)


print("only return doc")
print(c_generate_a_poem(title="The cat in the hat"))


@ai_task
def d_generate_a_poem(title: str):
    """
    Generate a poem based on the given title
    """
    return magic("poem", title)


print("only return name")
print(d_generate_a_poem(title="The cat in the hat"))


@ai_task
def f_generate_a_poem(title: str) -> str:
    """
    Generate a poem based on the given title
    :return: The generated poem
    """
    return magic(title)


print("return doc + return type")
print(f_generate_a_poem(title="The cat in the hat"))


@ai_task
def g_generate_a_poem(title: str) -> str:
    """
    Generate a poem based on the given title
    """
    return magic("poem", title)


print("return name + return type")
print(g_generate_a_poem(title="The cat in the hat"))


@ai_task
def generate_a_poem(title: str):
    """
    Generate a poem based on the given title
    :return: The generated poem
    """
    return magic("poem", title)


print("return doc + return name")
print(generate_a_poem(title="The cat in the hat"))


@ai_task
def h_generate_a_poem(title: str) -> str:
    """
    Generate a poem based on the given title
    :return: The generated poem
    """
    return magic("poem", title)


print("return all")
print(h_generate_a_poem(title="The cat in the hat"))
