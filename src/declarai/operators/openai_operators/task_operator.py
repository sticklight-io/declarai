import logging
from functools import partial
from typing import Callable, List, Optional, Type

from declarai.operators.base.types import Message, MessageRole
from declarai.operators.base.types.operator import BaseOperator, CompiledTemplate
from declarai.operators.shared.output_prompt import compile_output_prompt
from declarai.operators.shared.templates import (
    InstructFunctionTemplate,
    StructuredOutputInstructionPrompt,
)
from .openai_llm import OpenAILLM
from .openai_llm.llm_params import OpenAILLMParams

logger = logging.getLogger("OpenAITaskOperator")

INPUTS_TEMPLATE = "Inputs:\n{inputs}\n"
INPUT_LINE_TEMPLATE = "{param}: {{{param}}}"
NEW_LINE_INPUT_LINE_TEMPLATE = "\n{param}: {{{param}}}"


class OpenAITaskOperator(BaseOperator[OpenAILLMParams]):
    llm: OpenAILLM
    compiled_template: List[Message]
    set_llm: Callable

    @classmethod
    def new_operator(
        cls,
        openai_token: Optional[str] = None,
        model: Optional[str] = None,
    ) -> Type["OpenAITaskOperator"]:
        openai_llm = OpenAILLM(openai_token, model)
        partial_class = partial(cls, openai_llm)
        return partial_class

    def _compile_input_placeholder(self) -> str:
        """
        Creates a placeholder for the input of the function.
        The input format is based on the function input schema.

        for example a function signature of:
            def foo(a: int, b: str, c: float = 1.0):

        will result in the following placeholder:
            Inputs:
            a: {a}
            b: {b}
            c: {c}
        """
        inputs = ""

        if not self.parsed.signature_kwargs.keys():
            return inputs

        for i, param in enumerate(self.parsed.signature_kwargs.keys()):
            if i == 0:
                inputs += INPUT_LINE_TEMPLATE.format(param=param)
                continue
            inputs += NEW_LINE_INPUT_LINE_TEMPLATE.format(param=param)

        return INPUTS_TEMPLATE.format(inputs=inputs)

    def _compile_output_prompt(self, template) -> str:
        if not self.parsed.has_any_return_defs:
            logger.warning(
                "Couldn't create output schema for function %s."
                "Falling back to unstructured output."
                "Please add at least one of the following: return type, return doc, return name",
                self.parsed.name,
            )
            return ""

        signature_return = self.parsed.signature_return
        return_name, return_doc = self.parsed.docstring_return
        return compile_output_prompt(
            return_type=signature_return.str_schema,
            str_schema=return_name,
            return_docstring=return_doc,
            return_magic=self.parsed.magic.return_name,
            structured=self.parsed.has_structured_return_type,
            structured_template=template,
        )

    def compile_template(self) -> CompiledTemplate:
        instruction_template = InstructFunctionTemplate
        structured_template = StructuredOutputInstructionPrompt
        output_schema = self._compile_output_prompt(structured_template)

        messages = []
        if output_schema:
            messages.append(Message(message=output_schema, role=MessageRole.system))

        populated_instruction = instruction_template.format(
            input_instructions=self.parsed.docstring_freeform,
            input_placeholder=self._compile_input_placeholder(),
        )
        messages.append(Message(message=populated_instruction, role=MessageRole.user))
        return messages

    def compile(self, **kwargs) -> CompiledTemplate:
        template = self.compile_template()
        if kwargs:
            template[-1].message = template[-1].message.format(**kwargs)
            return {"messages": template}
        return {"messages": template}
