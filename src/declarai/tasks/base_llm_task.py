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
from typing import Any, TypeVar, Dict, Callable

from declarai.configurations.prompt_config import PromptConfig
from declarai.llm import LLM

logger = logging.getLogger("BaseFunction")


LLMTask = TypeVar("LLMTask", bound="BaseLLMTask")


class LLMTaskFuture:
    def __init__(self, exec_func: Callable[[], Any], populated_prompt: str):
        self.exec_func = exec_func
        self.__populated_prompt = populated_prompt

    def __call__(self) -> str:
        return self.exec_func(self.__populated_prompt)

    def get_populated_prompt(self) -> str:
        return self.__populated_prompt


class BaseLLMTask:
    use_ai = True

    def __init__(
        self,
        template: str,
        template_args: Dict[str, str],
        llm: LLM,
        prompt_config: PromptConfig = PromptConfig()
    ):
        self._llm = llm
        self._template = template
        self._template_args = template_args
        self._prompt_config = prompt_config

    def _exec_unstructured(self, prompt: str) -> str | None:
        logger.debug(prompt)
        result = self._llm.predict(prompt)
        return result

    def _exec_structured(self, prompt, multi_results: bool = False) -> Any:
        """
        Parses the generated data and returns the result.
        """
        logger.debug(prompt)
        raw_result = self._llm.predict(prompt)
        try:
            if multi_results:
                json_values = re.findall(r"{.*?}", raw_result, re.DOTALL)
            else:
                json_values = re.findall(r"{.*}", raw_result, re.DOTALL)

            serialized = {}
            for json_value in json_values:
                serialized_json_value = json.loads(json_value)
                serialized.update(serialized_json_value)
            return serialized["result"]

        except json.JSONDecodeError:
            logger.warning(
                "Failed to parse generated data\nplan: %s\ngenerated: %s",
                self._plan,
                raw_result,
            )
            return None

    def compile(self) -> str:
        """
        Generates the initial template to be used for later predictions.
        """
        logger.debug("Compiling task template")
        return self._template.format(**self._template_args)

    def _plan(self, **kwargs) -> str:
        logger.debug("Creating task plan (Injecting data into template)")
        return self.compile().format(**kwargs)

    def plan(self, **kwargs) -> LLMTaskFuture:
        """
        Populates the compiled template with the actual data.
        :param kwargs: the data to populate the template with
        """
        populated_prompt = self._plan(**kwargs)
        return LLMTaskFuture(self.exec, populated_prompt)

    def exec(self, populated_prompt: str) -> Any:
        """
        Executes the task.
        """
        logger.debug("Running planned task")
        if self._prompt_config.structured:
            return self._exec_structured(populated_prompt)
        return self._exec_unstructured(populated_prompt)

    def __call__(self, **kwargs):
        populated_prompt = self._plan(**kwargs)
        return self.exec(populated_prompt)
