import logging
from declarai.python_llm import ParsedFunction, FunctionLLMTranslator
from declarai.templates import StructuredOutputChatPrompt
from declarai.tasks.llm_chat import LLMChat
from declarai.templates.chat_template import CHAT_TEMPLATE

logger = logging.getLogger("LLMChatDecorator")


class LLMChatDecorator:
    def __init__(self, declarai_instance):
        self.declarai_instance = declarai_instance
        self.middlewares = []

    def __call__(
        self,
        func=None,
        *,
        middlewares: str = None,
    ):
        # When arguments are passed
        if func is None:
            self.middlewares = middlewares
            return self
        else:
            # When no arguments are passed
            return self._chat(func)

    def _chat(self, cls):
        parsed_function = ParsedFunction(cls)
        send_function = getattr(cls, "send", None)
        if send_function:
            send_parsed_function = ParsedFunction(send_function)
            llm_translator = FunctionLLMTranslator(send_parsed_function, StructuredOutputChatPrompt)
        else:
            logger.debug("No send function found. Using default LLMTranslator")
            llm_translator = FunctionLLMTranslator(parsed_function, StructuredOutputChatPrompt)

        greeting_prompt = getattr(cls, "greeting", None)

        system_prompt = parsed_function.docstring_freeform

        def llm_chat_factory(*args, **kwargs):
            system = kwargs.pop("system", system_prompt)
            greeting = kwargs.pop("greeting", greeting_prompt)

            llm_chat = LLMChat(
                template=CHAT_TEMPLATE,
                template_kwargs={
                    "system_prompt": system,
                    "output_instructions": llm_translator.compile_output_prompt(),
                },
                prompt_kwargs={
                    "structured": llm_translator.has_structured_return_type,
                    "return_name": llm_translator.return_name,
                    "return_type": llm_translator.return_type,
                },
                llm=self.declarai_instance.llm,
                middlewares=self.middlewares,
                greeting=greeting,
                *args,
                **kwargs,
            )
            llm_chat.__name__ = cls.__name__
            llm_chat.parsed_function = parsed_function
            llm_chat.llm_translator = llm_translator
            return llm_chat

        return llm_chat_factory
