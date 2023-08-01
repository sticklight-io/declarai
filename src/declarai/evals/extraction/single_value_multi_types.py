from typing import Dict, List

from declarai import Declarai


def single_value_multi_type_extraction(
    text: str, info_fields: List[str]
) -> Dict[str, str]:
    """
    Extract the provided info fields from the provided text
    :param text: content to extract info from
    :param info_fields: The information fields to extract
    :return: A mapping of extracted info field to the extracted value
    """
    return Declarai.magic(text=text, info_fields=info_fields)


single_value_multi_type_extraction_kwargs = {
    "text": "Hey jenny,\nyou can call me at 124-3435-132.\n",
    "info_fields": ["phone_number", "name"],
}
