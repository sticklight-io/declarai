from declarai.python_llm import FunctionLLMTranslator, ParsedFunction
from declarai.tasks.llm_task import LLMTask


class LLMTaskDecorator:
    def __init__(self, declarai_instance):
        self.declarai_instance = declarai_instance

    def __call__(
        self,
        func=None,
    ):
        # When arguments are passed
        if func is None:
            return self
        else:
            # When no arguments are passed
            return self._task(func)

    def _task(self, func):
        parsed_function = ParsedFunction(func)
        llm_translator = FunctionLLMTranslator(parsed_function)

        llm_task = LLMTask(
            template=llm_translator.template,
            template_kwargs={
                "input_instructions": llm_translator.parsed_func.docstring_freeform,
                "input_placeholder": llm_translator.compile_input_placeholder(),
                "output_instructions": llm_translator.compile_output_prompt(),
            },
            prompt_kwargs={
                "structured": llm_translator.has_any_return_defs,
                "return_name": llm_translator.return_name,
            },
            llm=self.declarai_instance.llm,
        )

        llm_task.__name__ = func.__name__

        llm_task.parsed_function = parsed_function
        llm_task.llm_translator = llm_translator

        return llm_task
