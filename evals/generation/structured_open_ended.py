from typing import Any, Dict, List

from declarai import Declarai


def structured_open_ended(name: str, skills: List[str]) -> Dict[str, Any]:
    """
    Generate a business profile based on the given name and skills
    Produce a short bio and a mapping of the skills and where they can be used
    :param name: The name of the person
    :param skills: The skills of the person
    :return: The generated business profile
    """
    return Declarai.magic(name=name, skills=skills)


structured_open_ended_kwargs = {
    "name": "Bob grapes",
    "skills": [
        "Management",
        "entrepreneurship",
        "programming",
        "investing",
        "Machine Learning",
    ],
}
