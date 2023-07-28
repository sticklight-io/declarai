from pprint import pprint
from typing import Dict, List

from pydantic import BaseModel

from declarai import Declarai


class TimeFrame(BaseModel):
    start: int
    end: int


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


def run_strict_complex_structured_generation(models: Dict[str, Declarai]):
    for model, declarai in models.items():

        @declarai.task
        def generate_business_profile(name: str, skills: List[str]) -> BusinessProfile:
            """
            Generate a business profile based on the given name and skills
            Produce a short bio and a mapping of the skills and where they can be used
            for fields with missing data, you can make up data to fill in the gaps
            :param name: The name of the person
            :param skills: The skills of the person
            :return: The generated business profile
            """
            return declarai.magic(name=name, skills=skills)

        res = generate_business_profile(
            name="Bob grapes",
            skills=[
                "Management",
                "entrepreneurship",
                "programming",
                "investing",
                "Machine Learning",
            ],
        )

        print(model + " generate profile:")
        pprint(res)
