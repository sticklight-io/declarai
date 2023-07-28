from typing import Dict

from declarai import Declarai


def run_unstructured_longform_generation(models: Dict[str, Declarai]):
    for model, declarai in models.items():

        @declarai.task
        def generate_poem(title: str) -> str:
            """
            Write a poem based on the given title
            The poem should have 4 verses
            """
            return declarai.magic(title)

        res = generate_poem(title="Using LLMs is fun!")

        print(model + " write a poem:")
        print(res)
