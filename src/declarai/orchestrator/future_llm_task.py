from typing import Any, Callable, Dict


class FutureLLMTask:
    def __init__(
        self,
        exec_func: Callable[[str], Any],
        kwargs: Dict[str, Any],
        compiled_template: str,
        populated_prompt: str,
    ):
        self.exec_func = exec_func
        self.__populated_prompt = populated_prompt
        self.__compiled_template = compiled_template
        self.__kwargs = kwargs

    def __call__(self) -> str:
        return self.exec_func(self.__populated_prompt)

    @property
    def populated_prompt(self) -> str:
        return self.__populated_prompt

    @property
    def compiled_template(self) -> str:
        return self.__compiled_template

    @property
    def task_kwargs(self) -> Dict[str, Any]:
        return self.__kwargs
