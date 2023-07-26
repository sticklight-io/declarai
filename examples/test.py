from typing import Dict, List

from declarai import init_declarai, magic, Sequence

ai_task = init_declarai(provider="openai", model="gpt-3.5-turbo")


@ai_task
def extract_email_contacts(text: str, contact_fields: List[str]) -> Dict[str, str]:
    return magic(
        "contacts",
        task_desc="Extract contact fields from text",
        input_desc={
            "text": "The text to extract contact information from",
            "contact_fields": "The contact fields to extract",
        },
        output_desc="A mapping of the contact fields to their values",
        text=text,
        contact_fields=contact_fields,
    )


@ai_task
def anonymize_data(data: Dict[str, str]) -> Dict[str, str]:
    """
    Redact any potentially private data in the input with "***"
    :param data: The data to anonymize
    :return: The anonymized data
    """
    return magic(data)


contact_data = extract_email_contacts.plan(
    text="I am John Doe and my phone number is 123-456-7890. ",
    contact_fields=["phone", "name", "email"],
)

anonymized = anonymize_data.plan(data=contact_data)
reduced_task = Sequence(anonymized, reduce_strategy="CoT")
anonymized_data = reduced_task()
print(anonymized_data)
