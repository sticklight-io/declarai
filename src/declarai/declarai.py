from typing import Optional, overload

from declarai.decorators.chat_decorator import LLMChatDecorator
from declarai.decorators.magic import magic
from declarai.decorators.task_decorator import LLMTaskDecorator
from declarai.operators import LLMSettings, ModelsOpenai, ProviderOpenai


class Declarai:
    """
    A root interface to declarai.
    This class allows creating tasks and other declarai provided tools.
    """

    magic = magic

    # *-------------------------------------------------------------------------- *
    # * Custom overloads to enforce the relationship between PROVIDER and MODELS  *
    # * Additionally supported providers should be exposed via the Declarai class *
    # * here:                                                                     *
    # *-------------------------------------------------------------------------- *
    @overload
    def __init__(
        self,
        provider: ProviderOpenai,
        model: ModelsOpenai,
        version: Optional[str] = None,
        openai_token: Optional[str] = None,
    ):
        ...

    # *-------------------------------------------------------------------------- *
    # * Actual implementation of Declarai                                         *
    # *-------------------------------------------------------------------------- *
    def __init__(self, **kwargs):
        self.llm_config = LLMSettings(**kwargs)

        self.task = LLMTaskDecorator(self, **kwargs)

        class Experimental:
            chat = LLMChatDecorator(self, **kwargs)

        self.experimental = Experimental
