# from declarai.api.chat_decorator import LLMChatDecorator
from declarai.api.chat_decorator import LLMChatDecorator
from declarai.api.magic import magic
from declarai.api.task_decorator import LLMTaskDecorator
from declarai.operators import LLMSettings


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
    # TODO: Move this?
    # @overload
    # def __init__(
    #     self,
    #     provider: ProviderOpenai,
    #     model: ModelsOpenai,
    #     version: Optional[str] = None,
    #     openai_token: Optional[str] = None,
    # ):
    #     ...

    # *-------------------------------------------------------------------------- *
    # * Actual implementation of Declarai                                         *
    # *-------------------------------------------------------------------------- *
    def __init__(self, **kwargs):
        self.llm_config = LLMSettings(**kwargs)

        self.task = LLMTaskDecorator(self)

        class Experimental:
            chat = LLMChatDecorator(self)

        self.experimental = Experimental
