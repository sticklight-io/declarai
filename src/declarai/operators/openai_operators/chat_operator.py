import logging
from functools import partial
from typing import List, Optional, Type
from typing_extensions import Self

from declarai.operators.base.types import Message, MessageRole
from declarai.operators.base.types.operator import CompiledTemplate, BaseOperator
from declarai.operators.shared.output_prompt import compile_output_prompt
from declarai.operators.shared.templates import StructuredOutputChatPrompt
from declarai.python_parser.parser import PythonParser

from .openai_llm import OpenAILLM
from .openai_llm import OpenAILLMParams

logger = logging.getLogger("OpenAIChatOperator")


class OpenAIChatOperator(BaseOperator[OpenAILLMParams]):
    llm: OpenAILLM
    compiled_template: List[Message]

    @classmethod
    def new_operator(
        cls,
        openai_token: Optional[str] = None,
        model: Optional[str] = None,
    ) -> Type["OpenAIChatOperator"]:
        openai_llm = OpenAILLM(openai_token, model)
        partial_class: Self = partial(cls, openai_llm)
        return partial_class

    def __init__(
        self,
        llm: OpenAILLM,
        parsed: PythonParser,
        parsed_func: PythonParser,
        **kwargs,
    ):
        super().__init__(llm=llm, parsed=parsed, **kwargs)
        self.parsed_func = parsed_func
        self.system = kwargs.get("system", self.parsed.docstring_freeform)

    def _compile_output_prompt(self, template) -> str:
        if not self.parsed_func.has_any_return_defs:
            logger.warning(
                "Couldn't create output schema for function %s."
                "Falling back to unstructured output."
                "Please add at least one of the following: return type, return doc, return name",
                self.parsed_func.name,
            )
            return ""

        signature_return = self.parsed_func.signature_return
        return_name, return_doc = self.parsed_func.docstring_return
        return compile_output_prompt(
            return_type=signature_return.str_schema,
            str_schema=return_name,
            return_docstring=return_doc,
            return_magic=self.parsed_func.magic.return_name,
            structured=self.parsed_func.has_structured_return_type,
            structured_template=template,
        )

    def compile(self, messages: List[Message], **kwargs) -> CompiledTemplate:
        self.system = self.system.format(**kwargs)
        structured_template = StructuredOutputChatPrompt
        if self.parsed_func:
            output_schema = self._compile_output_prompt(structured_template)
        else:
            output_schema = None

        if output_schema:
            compiled_system_prompt = f"{self.system}/n{output_schema}"
        else:
            compiled_system_prompt = self.system
        messages = [
                       Message(message=compiled_system_prompt, role=MessageRole.system)
                   ] + messages
        return {"messages": messages}
