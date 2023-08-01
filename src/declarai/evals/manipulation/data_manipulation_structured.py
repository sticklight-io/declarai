from typing import Dict

from declarai import Declarai


def data_manipulation(data: Dict[str, str]) -> Dict[str, str]:
    """
    return a redacted version of the input data
    any potentially private data in the input should be replaced with "***"
    :param data: The data to anonymize
    :return: The anonymized data
    """
    return Declarai.magic("redacted_info", data=data)


data_manipulation_kwargs = {
    "data": {
        "name": "John Doe",
        "phone": "123-456-7890",
        "email": "john.doe@coolmail.com",
        "address": "9493 south bridge St.",
    }
}
