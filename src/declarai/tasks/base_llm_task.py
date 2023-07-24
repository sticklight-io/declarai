"""BaseLLMTask

Provides the most basic component to interact with an LLM.
LLMs are ofter interacted with via an API. In order to provide prompts and receive predictions,
we will need to create the following:
- A prompt template that will be populated with the data to be passed to the model
- A method to generate the data
- Optionally a parser to parse the generated data
"""
import json
import logging
import re
from typing import Any

from declarai.configurations.prompt_config import PromptConfig
from declarai.llm import LLM

logger = logging.getLogger("BaseFunction")


class BaseLLMTask:
    def __init__(
        self, template: str, llm: LLM, prompt_config: PromptConfig = PromptConfig()
    ):
        self.llm = llm
        self.generation_template = template
        self.prompt_config = prompt_config

    def populate_template(
        self,
        **kwargs,
    ) -> str:
        """
        Populates the provided data_generation_template with the actual data.
        :param kwargs: the data to populate the template with
        :return: the populated data_generation_prompt to pass to the model
        """
        return self.generation_template.format(**kwargs)

    def generate_unstructured(self, prompt: str) -> str | None:
        logger.debug(prompt)
        generated = self.llm.predict(prompt)
        return generated

    def generate_structured(self, prompt: str, multi_results: bool = False) -> Any:
        logger.debug(prompt)
        generated = self.llm.predict(prompt)
        try:
            if multi_results:
                json_values = re.findall(r"{.*?}", generated, re.DOTALL)
            else:
                json_values = re.findall(r"{.*}", generated, re.DOTALL)

            serialized = {}
            for json_value in json_values:
                serialized_json_value = json.loads(json_value)
                serialized.update(serialized_json_value)
            return serialized

        except json.JSONDecodeError:
            logger.warning(
                "Failed to parse generated data\nprompt: %s\ngenerated: %s",
                prompt,
                generated,
            )

    def generate(
        self,
        **kwargs,
    ) -> Any:
        logger.debug("Generating task result")
        data_generation_prompt = self.populate_template(**kwargs)
        if self.prompt_config.structured:
            return self.generate_structured(data_generation_prompt)
        return self.generate_unstructured(data_generation_prompt)
