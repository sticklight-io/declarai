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

from declarai.clients.openai_client import OpenAIClient
from declarai.configurations.llm_config import LLMConfig
from declarai.configurations.prompt_config import PromptConfig

logger = logging.getLogger("BaseFunction")


class BaseLLMTask:
    prompt_config: PromptConfig = PromptConfig()
    llm_config: LLMConfig = LLMConfig()

    def __init__(self, template: str):
        self.openai = OpenAIClient()
        self.generation_template = template

    def generation_prompt(
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
        generated = self.openai.predict(prompt)
        return generated

    def generate_structured(self, prompt: str, multi_results: bool = False) -> Any:
        logger.debug(prompt)
        generated = self.openai.predict(prompt)
        try:
            if multi_results:
                json_values = re.findall(r"{.*?}", generated, re.DOTALL)
            else:
                json_values = re.findall(r"{.*}", generated, re.DOTALL)
            res = {}
            for v in json_values:
                raw_res = json.loads(v)
                res.update(raw_res)
            return res
        except json.JSONDecodeError:
            logger.warning(
                f"Failed to parse generated data\nprompt: {prompt}\ngenerated: {generated}"
            )

    def generate(
        self,
        **kwargs,
    ) -> Any:
        logger.info("Generating data")
        data_generation_prompt = self.generation_prompt(**kwargs)
        if self.prompt_config.structured:
            return self.generate_structured(data_generation_prompt)
        return self.generate_unstructured(data_generation_prompt)
