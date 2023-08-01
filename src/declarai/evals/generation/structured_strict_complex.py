from typing import List, Optional

from pydantic import BaseModel

from declarai import Declarai


class TimeFrame(BaseModel):
    start: int
    end: Optional[int]


class BusinessTrait(BaseModel):
    time_frame: TimeFrame
    title: str
    description: str
    experience: str


class Recommendation(BaseModel):
    recommender: str
    recommendation: str


class BusinessProfile(BaseModel):
    bio: str
    traits: List[BusinessTrait]
    previous_jobs: List[str]
    recommendations: List[Recommendation]


def structured_strict_complex(name: str, skills: List[str]) -> BusinessProfile:
    """
    Generate a business profile based on the given name and skills
    Produce a short bio and a mapping of the skills and where they can be used
    for fields with missing data, you can make up data to fill in the gaps
    :param name: The name of the person
    :param skills: The skills of the person
    :return: The generated business profile
    """
    return Declarai.magic(name=name, skills=skills)


structured_strict_complex_kwargs = {
    "name": "Bob grapes",
    "skills": [
        "Management",
        "entrepreneurship",
        "programming",
        "investing",
        "Machine Learning",
    ],
}
