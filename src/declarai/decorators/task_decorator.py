from declarai.python_parsers.function_parser import PythonParser
from declarai.operators.templates import StructuredOutputInstructionPrompt
from declarai.tasks.llm_task import LLMTask


class LLMTaskDecorator:
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
            return self._task(func)

    def _task(self, func):
        parsed_function = PythonParser(func)
        llm_translator = FunctionLLMTranslator(
            parsed_function, StructuredOutputInstructionPrompt
        )

        llm_task = LLMTask(
            template=llm_translator.template,
            template_kwargs={
                "input_instructions": llm_translator.parsed_func.docstring_freeform,
                "input_placeholder": llm_translator.compile_input_placeholder(),
            },
            prompt_kwargs={
                "structured": llm_translator.has_structured_return_type,
                "return_name": llm_translator.return_name,
                "return_schema": llm_translator.compile_output_prompt(),
                "return_type": llm_translator.return_type,
            },
            llm=self.declarai_instance.llm,
            middlewares=self.middlewares,
        )

        llm_task.__name__ = func.__name__

        llm_task.parsed_function = parsed_function
        llm_task.llm_translator = llm_translator

        return llm_task
