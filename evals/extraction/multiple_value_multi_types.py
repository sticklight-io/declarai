from typing import Dict, List

from declarai import Declarai


def multi_value_multi_type_extraction(
    text: str, info_fields: List[str]
) -> Dict[str, str]:
    """
    Extract the phone number from the provided text
    :param text: content to extract phone number from
    :param info_fields: The information fields to extract
    :return: The phone numbers that are used in the email
    """
    return Declarai.magic(text=text, info_fields=info_fields)


multi_value_multi_type_extraction_kwargs = {
    "text": "Hey jenny,\nyou can call me at 124-3435-132.\n"
    "you can also reach me at +43-938-243-223",
    "info_fields": ["phone_number", "name"],
}
