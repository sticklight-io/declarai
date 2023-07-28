from typing import Dict

from declarai import Declarai


def run_structured_generation(models: Dict[str, Declarai]):
    for model, declarai in models.items():

        @declarai.task
        def write_a_poem(title: str) -> Dict[str, str]:
            """
            Create a player profile
            """
            return declarai.magic(title)

        res = write_a_poem(title="Using LLMs is fun!")

        print(model + " write a poem:")
        print(res)
