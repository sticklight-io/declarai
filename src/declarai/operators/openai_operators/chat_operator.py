"""
Chat implementation of OpenAI operator.
"""
import logging
from declarai.operators.openai_operators.openai_llm import AzureOpenAILLM, OpenAILLM
from declarai.operators.operator import BaseChatOperator
from declarai.operators.registry import register_operator

logger = logging.getLogger("OpenAIChatOperator")


@register_operator(provider="openai", operator_type="chat")
class OpenAIChatOperator(BaseChatOperator):
    """
    Chat implementation of OpenAI operator. This is a child of the BaseChatOperator class. See the BaseChatOperator class for further documentation.

    Attributes:
        llm: OpenAILLM
    """

    llm: OpenAILLM


@register_operator(provider="azure-openai", operator_type="chat")
class AzureOpenAIChatOperator(OpenAIChatOperator):
    """
    Chat implementation of OpenAI operator. This is a child of the BaseChatOperator class. See the BaseChatOperator class for further documentation.

    Attributes:
        llm: AzureOpenAILLM
    """

    llm: AzureOpenAILLM
