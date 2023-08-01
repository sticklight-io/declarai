from typing import List

from declarai import Declarai


def multi_value_extraction(text: str) -> List[str]:
    """
    Extract the phone numbers from the provided text
    :param text: content to extract phone number from
    :return: The phone numbers that where identified in the input text
    """
    return Declarai.magic(text=text)


multi_value_extraction_kwargs = {
    "text": "Hey jenny,\nyou can call me at 124-3435-132.\n"
    "you can also reach me at +43-938-243-223"
}
