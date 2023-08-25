"""
Chat implementation of OpenAI operator.
"""
import logging
from typing import List

from declarai.operators import Message, MessageRole
from declarai.operators.openai_operators.openai_llm import AzureOpenAILLM, OpenAILLM
from declarai.operators.operator import BaseChatOperator, CompiledTemplate
from declarai.operators.registry import register_operator
from declarai.operators.templates import (
    StructuredOutputChatPrompt,
    compile_output_prompt,
)

logger = logging.getLogger("OpenAIChatOperator")


@register_operator(provider="openai", operator_type="chat")
class OpenAIChatOperator(BaseChatOperator):
    """
    Chat implementation of OpenAI operator. This is a child of the BaseChatOperator class. See the BaseChatOperator class for further documentation.

    Attributes:
        llm: OpenAILLM
    """

    llm: OpenAILLM

    def _compile_output_prompt(self, template) -> str:
        if not self.parsed_send_func.has_any_return_defs:
            logger.warning(
                "Couldn't create output schema for function %s."
                "Falling back to unstructured output."
                "Please add at least one of the following: return type, return doc, return name",
                self.parsed_send_func.name,
            )
            return ""

        signature_return = self.parsed_send_func.signature_return
        return_name, return_doc = self.parsed_send_func.docstring_return
        return compile_output_prompt(
            return_type=signature_return.str_schema,
            str_schema=return_name,
            return_docstring=return_doc,
            return_magic=self.parsed_send_func.magic.return_name,
            structured=self.parsed_send_func.has_structured_return_type,
            structured_template=template,
        )

    def compile(self, messages: List[Message], **kwargs) -> CompiledTemplate:
        """
        Implementation of the compile method for the chat operator.
        Compiles a system prompt based on the initialized system message
        Compiles the message based on the user input and the StructuredOutputChatPrompt template
        Args:
            messages (List[Message]): A list of messages
            **kwargs:

        Returns:

        """
        self.system = self.system.format(**kwargs)
        structured_template = StructuredOutputChatPrompt
        if self.parsed_send_func:
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


@register_operator(provider="azure-openai", operator_type="chat")
class AzureOpenAIChatOperator(OpenAIChatOperator):
    """
    Chat implementation of OpenAI operator. This is a child of the BaseChatOperator class. See the BaseChatOperator class for further documentation.

    Attributes:
        llm: AzureOpenAILLM
    """

    llm: AzureOpenAILLM
