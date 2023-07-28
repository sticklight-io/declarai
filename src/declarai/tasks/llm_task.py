"""LLMTask

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
from typing import Any, Dict, Optional, TypeVar

from declarai.llm import LLM
from declarai.llm.settings import PromptSettings

from .future_task import FutureLLMTask

logger = logging.getLogger("BaseFunction")


LLMTaskType = TypeVar("LLMTaskType", bound="LLMTask")


class LLMTask:
    use_ai = True

    def __init__(
        self,
        template: str,
        template_kwargs: Dict[str, str],
        llm: LLM,
        prompt_kwargs: Optional[Dict[str, Any]] = None,
    ):
        self._llm = llm
        self._template = template
        self._template_args = template_kwargs
        if not prompt_kwargs:
            prompt_kwargs = {}
        self._prompt_config = PromptSettings(**prompt_kwargs)

    def _exec_unstructured(self, prompt: str) -> Optional[str]:
        logger.debug(prompt)
        result = self._llm.predict(prompt)
        return result

    def _exec_structured(self, prompt) -> Any:
        """
        Parses the generated data and returns the result.
        """
        logger.debug(prompt)
        raw_result = self._llm.predict(prompt)
        try:
            if self._prompt_config.multi_results:
                json_values = re.findall(r"{.*?}", raw_result, re.DOTALL)
                serialized = {}
                for json_value in json_values:
                    serialized_json_value = json.loads(json_value)
                    serialized.update(serialized_json_value)
                return serialized
            else:
                json_values = re.findall(r"{.*}", raw_result, re.DOTALL)
                serialized = {}
                for json_value in json_values:
                    serialized_json_value = json.loads(json_value)
                    serialized.update(serialized_json_value)
                if self._prompt_config.return_name in serialized:
                    return serialized[self._prompt_config.return_name]
                return serialized

        except json.JSONDecodeError:
            logger.warning(
                "Failed to parse generated data\nplan: %s\ngenerated: %s",
                self._plan,
                raw_result,
            )
            return None

    def compile(self, **kwargs) -> str:
        """
        Generates the initial template to be used for later predictions.
        Optionally passing kwargs will also inject the data into the compiled template.
        """
        logger.debug("Compiling task template")
        template = self._template.format(**self._template_args)
        if kwargs:
            template = template.format(**kwargs)
        return template

    def _plan(self, **kwargs) -> str:
        logger.debug("Creating task plan (Injecting data into template)")
        return self.compile().format(**kwargs)

    def plan(self, **kwargs) -> FutureLLMTask:
        """
        Populates the compiled template with the actual data.
        :param kwargs: the data to populate the template with
        """
        populated_prompt = self._plan(**kwargs)
        return FutureLLMTask(
            self._exec,
            kwargs=kwargs,
            compiled_template=self.compile(),
            populated_prompt=populated_prompt,
        )

    def _exec(self, populated_prompt: str) -> Any:
        """
        Executes the task.
        """
        logger.debug("Running planned task")
        if self._prompt_config.structured:
            return self._exec_structured(populated_prompt)
        return self._exec_unstructured(populated_prompt)

    def __call__(self, **kwargs):
        populated_prompt = self._plan(**kwargs)
        return self._exec(populated_prompt)
