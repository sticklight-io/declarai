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
from json import JSONDecodeError
from typing import Any, Dict, List, Optional

from pydantic.tools import parse_obj_as, parse_raw_as

from declarai.operators.llm import LLM
from declarai.operators.llm import LLMResponse
from declarai.operators.llm import PromptSettings
from declarai.middlewares.base import TaskMiddleware
from .chat.message import Message

from .future_task import FutureLLMTask

logger = logging.getLogger("BaseFunction")


class LLMTask:
    use_ai = True

    def __init__(
        self,
        template: str,
        template_kwargs: Dict[str, str],
        llm: LLM,

        middlewares: Optional[List[TaskMiddleware]] = None,
    ):
        self.llm = llm
        self.template = template
        self.template_args = template_kwargs
        if not prompt_kwargs:
            prompt_kwargs = {}
        self.prompt_config = PromptSettings(**prompt_kwargs)
        self.middlewares = middlewares or []

        self.llm_response: Optional[LLMResponse] = None
        self.result: Any = None
        self.call_kwargs: Dict[str, Any] = {}

    def _predict(self, prompt, system_prompt: Optional[str] = None) -> LLMResponse:
        messages = []
        if system_prompt:
            messages.append(Message(
                message=system_prompt,
                role="system",
            ))
        messages.append(Message(
            message=prompt,
            role="user",
        ))
        return self.llm.predict(messages)

    def _exec_unstructured(self, prompt: str) -> Optional[Any]:
        logger.debug(prompt)
        if self.prompt_config.return_schema:
            llm_result = self._predict(prompt, self.prompt_config.return_schema)
        else:
            llm_result = self._predict(prompt)
        if self.prompt_config.return_type:
            try:
                return parse_raw_as(self.prompt_config.return_type, llm_result.response)
            except JSONDecodeError:
                return parse_obj_as(self.prompt_config.return_type, llm_result.response)
        return llm_result.response

    def _exec_structured(self, prompt) -> Any:
        """
        Parses the generated data and returns the result.
        """
        logger.debug(prompt)
        self.llm_response = self._predict(
            prompt, system_prompt=self.prompt_config.return_schema
        )
        raw_result = self.llm_response.response
        try:
            if self.prompt_config.multi_results:
                json_values = re.findall(r"{.*?}", raw_result, re.DOTALL)
                serialized = {}
                for json_value in json_values:
                    clean_value = json_value.replace("```json", "").replace("```", "")
                    serialized_json_value = json.loads(clean_value)
                    serialized.update(serialized_json_value)
                return serialized
            else:
                parsed_result = parse_raw_as(dict, raw_result)
                root_key = self.prompt_config.return_name or "declarai_result"
                parsed_result = parsed_result[root_key]

                return parse_obj_as(self.prompt_config.return_type, parsed_result)

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
        template = self.template.format(**self.template_args)
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

    def _exec_task(self, populated_prompt: str) -> Any:
        """
        Executes the task.
        """
        logger.debug("Running planned task")
        if self.prompt_config.structured:
            self.result = self._exec_structured(populated_prompt)
        else:
            self.result = self._exec_unstructured(populated_prompt)
        return self.result

    def _exec(self, populated_prompt: str) -> Any:
        if self.middlewares:
            for middleware in self.middlewares:
                exec_with_middlewares = middleware(self, populated_prompt)
            return exec_with_middlewares()
        return self._exec_task(populated_prompt)

    def __call__(self, **kwargs) -> Any:
        self.call_kwargs = kwargs
        populated_prompt = self._plan(**kwargs)
        return self._exec(populated_prompt)
