import os
from typing import List

from declarai.operators.base import Operator
from declarai.operators.llm import OpenAILLM
from declarai.operators.output_prompt import compile_output_prompt
from declarai.operators.templates import InstructFunctionTemplate, StructuredOutputInstructionPrompt
from declarai.orchestrator.orchestrator import INPUT_LINE_TEMPLATE, NEW_LINE_INPUT_LINE_TEMPLATE, INPUTS_TEMPLATE, \
    logger, CompiledTemplate
from declarai.python_parsers.function_parser import PythonParser
from declarai.tasks.chat.message import Message


class OpenAIOperator(Operator):
    llm: OpenAILLM
    compiled_template: List[Message]

    def __init__(self, parsed: PythonParser):
        super().__init__(parsed)
        self.llm = OpenAILLM(
            openai_token=os.getenv("DECLARAI_OPENAI_API_KEY"), model="gpt-3.5-turbo"
        )

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
            system_prompt = structured_template.format(
                output_schema=output_schema,
                return_name=self.parsed.return_name,
            )
            messages.append(Message(message=system_prompt, role="system"))

        populated_instruction = instruction_template.format(
            input_instructions=self.parsed.docstring_freeform,
            input_placeholder=self._compile_input_placeholder(),
        )
        messages.append(Message(message=populated_instruction, role="user"))
        return messages

    def compile(self, **kwargs) -> CompiledTemplate:
        template = self.compile_template()
        if kwargs:
            template[-1].message = template[-1].message.format(**kwargs)
            return template
        return template

    def predict(self, **kwargs) -> str:
        llm_response = self.llm.predict(self.compile(**kwargs), **self.llm_params)
        return llm_response.response
