from typing import Dict, List

from declarai import Sequence, init_declarai, magic

ai_task = init_declarai(provider="openai", model="gpt-3.5-turbo-0301")


@ai_task
def extract_email_info(text: str, contact_fields: List[str]) -> Dict[str, str]:
    """
    Don't write python code

    Extract the provided contact fields from the given text
    :param text: The text to extract contact information from
    :param contact_fields: The contact fields to extract
    :return: A mapping of the contact fields to their values
    """
    return magic("email_info", text, contact_fields)


@ai_task
def anonymize_data(data: Dict[str, str]) -> Dict[str, str]:
    """
    return a redacted version of the input data
    any potentially private data in the input should be replaced with "***"
    :param data: The data to anonymize
    :return: The anonymized data
    """
    return magic("redacted_info", data)


contact_data = extract_email_info.plan(
    text="I am John Doe and my phone number is 123-456-7890. ",
    contact_fields=["phone", "name", "email"],
)
anonymized = anonymize_data.plan(data=contact_data)

reduced_task = Sequence(anonymized, reduce_strategy="CoT")
anonymized_data = reduced_task()
print(anonymized_data)
# print(anonymized)
