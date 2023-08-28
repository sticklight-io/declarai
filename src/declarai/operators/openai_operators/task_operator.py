"""
Task implementation for openai operator.
"""
import logging

from declarai.operators.registry import register_operator
from declarai.operators.message import Message, MessageRole
from declarai.operators.operator import BaseOperator, CompiledTemplate
from declarai.operators.templates import (
    InstructFunctionTemplate,
    StructuredOutputInstructionPrompt,
    compile_output_prompt,
)

from .openai_llm import AzureOpenAILLM, OpenAILLM

logger = logging.getLogger("OpenAITaskOperator")

INPUTS_TEMPLATE = "Inputs:\n{inputs}\n"
INPUT_LINE_TEMPLATE = "{param}: {{{param}}}"
NEW_LINE_INPUT_LINE_TEMPLATE = "\n{param}: {{{param}}}"


@register_operator(provider="openai", operator_type="task")
class OpenAITaskOperator(BaseOperator):
    """
    Task implementation for openai operator. This is a child of the BaseOperator class. See the BaseOperator class for further documentation.
    Implements the compile method which compiles a parsed function into a message.
    Uses the OpenAILLM to generate a response based on the given template.

    Attributes:
        llm: OpenAILLM
    """

    llm: OpenAILLM

    def _compile_input_placeholder(self) -> str:
        """
        Creates a placeholder for the input of the function.
        The input format is based on the function input schema.

        !!! example
            for example a function signature of:
                ```py
                def foo(a: int, b: str, c: float = 1.0):
                ```

            will result in the following placeholder:
            ```md
                Inputs:
                a: {a}
                b: {b}
                c: {c}
            ```
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
        """
        Unique compilation method for the OpenAITaskOperator class.
        Uses the InstructFunctionTemplate and StructuredOutputInstructionPrompt templates to create a message.
        And the _compile_input_placeholder method to create a placeholder for the input of the function.
        Returns:
            Dict[str, List[Message]]: A dictionary containing a list of messages.

        """
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
        """
        Implements the compile method of the BaseOperator class.
        Args:
            **kwargs:

        Returns:
            Dict[str, List[Message]]: A dictionary containing a list of messages.

        """
        template = self.compile_template()
        if kwargs:
            template[-1].message = template[-1].message.format(**kwargs)
            return {"messages": template}
        return {"messages": template}


@register_operator(provider="azure-openai", operator_type="task")
class AzureOpenAITaskOperator(OpenAITaskOperator):
    """
    Task implementation for openai operator that uses Azure as the llm provider.

    Attributes:
        llm: AzureOpenAILLM
    """

    llm: AzureOpenAILLM
