from typing import List, Dict

from declarai import Declarai


def run_multi_value_extraction_eval(models: Dict[str, Declarai]):
    for model, declarai in models.items():

        @declarai.task
        def extract_phone_number(text: str) -> List[str]:
            """
            Extract the phone number from the provided text
            :param text: content to extract phone number from
            :return: The phone numbers that are used in the email
            """
            return declarai.magic(text=text)

        res = extract_phone_number(
            text="Hey jenny,\nyou can call me at 124-3435-132.\n"
            "you can also reach me at +43-938-243-223"
        )

        print(model + " phone number extraction:")
        print(res)
