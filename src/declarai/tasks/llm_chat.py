import json
import logging
import re
from json import JSONDecodeError
from typing import Dict, Optional, Any, List, Union

from pydantic.tools import parse_raw_as, parse_obj_as

from declarai.operators.llm import LLM
from declarai.operators.llm import LLMResponse
from declarai.operators.llm import PromptSettings
from declarai.middlewares.base import TaskMiddleware
from declarai.tasks.chat.message import Message

logger = logging.getLogger("LLMChat")


class LLMChat:
    def __init__(self,
                 template: str,
                 template_kwargs: Dict[str, str],
                 llm: LLM,
                 prompt_kwargs: Optional[Dict[str, Any]] = None,
                 middlewares: Optional[List[TaskMiddleware]] = None,
                 greeting: Optional[str] = None,
                 system: Optional[str] = None,
                 ):
        self.llm = llm
        self.template = template
        self.template_args = template_kwargs
        if system:
            self.template_args["system_prompt"] = system
        if not prompt_kwargs:
            prompt_kwargs = {}
        self.prompt_config = PromptSettings(**prompt_kwargs)
        self.middlewares = middlewares or []
        self.__system_message: Optional[Message] = None
        self.__messages: List[Message] = []
        self._greeting_message = self.format_message(greeting, "assistant") if greeting else None

        self.llm_response: Optional[LLMResponse] = None
        self.last_compiled_messages: Optional[List[Message]] = None
        self.result: Any = None
        self.call_kwargs: Dict[str, Any] = {}

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    @property
    def conversation(self):
        if self._greeting_message:
            return [self._greeting_message] + self.__messages
        return self.__messages

    @property
    def _system_message(self) -> Message:
        if not self.__system_message:
            self.__system_message = Message(self.template.format(**self.template_args),
                                            "system")
        return self.__system_message

    @property
    def greeting(self) -> str:
        if self._greeting_message:
            return repr(self._greeting_message)

    @property
    def system(self) -> str:
        if self._system_message:
            return repr(self._system_message)

    @staticmethod
    def format_message(prompt: str, role: str) -> Message:
        return Message(prompt, role)

    def _exec_unstructured(self, messages: List[Message]) -> Optional[Any]:
        self.llm_response = self.llm.predict(messages=messages)
        raw_result = self.llm_response.response
        if self.prompt_config.return_type:
            try:
                return parse_raw_as(self.prompt_config.return_type, raw_result)
            except JSONDecodeError:
                return parse_obj_as(self.prompt_config.return_type, raw_result)
        return raw_result

    def _exec_structured(self, messages: List[Message]) -> Any:
        """
        Parses the generated data and returns the result.
        """
        logger.debug(messages)
        self.llm_response = self.llm.predict(messages=messages)
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

    def _compile_messages(self) -> List[Message]:
        system_message = self._system_message
        messages = []
        if system_message:
            messages.append(system_message)
        if self.conversation:
            messages += self.conversation

        return messages

    def compile(self, return_prompt: bool = False, message: Optional[str] = None, role: Optional[str] = "user",
                **kwargs) -> Union[str, List[Message]]:
        """
        Generates the initial template to be used for later predictions.
        Optionally passing kwargs will also inject the data into the compiled template.
        """
        logger.debug("Compiling task template")
        system_message = self._system_message
        if kwargs:
            system_message.message = system_message.message.format(**kwargs)

        messages = self._compile_messages()
        if message:
            messages += [self.format_message(message, role)]
        if return_prompt:
            prompt = ""
            for i in messages:
                prompt += f"{repr(i)}\n"
            return prompt
        return messages

    def _plan(self, **kwargs) -> str:
        logger.debug("Creating task plan (Injecting data into template)")
        return self.compile(**kwargs)

    def _exec_task(self, messages) -> Any:
        """
        Executes the task.
        """
        logger.debug("Running planned task")
        self.last_compiled_messages = messages
        if self.prompt_config.structured:
            self.result = self._exec_structured(messages)
        else:
            self.result = self._exec_unstructured(messages)
        return self.result

    def _exec(self, messages) -> Any:
        if self.middlewares:
            for middleware in self.middlewares:
                exec_with_middlewares = middleware(self, messages)
            return exec_with_middlewares()
        return self._exec_task(messages)

    def send(self, message: str, **kwargs) -> Any:
        self.call_kwargs = kwargs
        messages = self._plan(**kwargs, message=message)
        result = self._exec(messages)
        self.add_message(message, "user")
        self.add_message(result, "assistant")
        return result

    def add_message(self, message: str, role: str) -> None:
        self.__messages.append(self.format_message(message, role))

    def __enter__(self):
        print(self.greeting)
        return self

    def __exit__(self, type, value, traceback):
        print("Goodbye!")
