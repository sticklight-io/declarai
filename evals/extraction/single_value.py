from typing import List

from declarai import Declarai


def single_value_extraction(text: str) -> List[str]:
    """
    Extract the phone number from the provided text
    :param text: content to extract phone number from
    :return: The phone numbers that are used in the email
    """
    return Declarai.magic(text=text)


single_value_extraction_kwargs = {
    "text": "Hey jenny,\nyou can call me at 124-3435-132.\n"
}
