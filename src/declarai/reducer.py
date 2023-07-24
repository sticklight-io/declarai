"""Reducer

The reducer allows chaining together a collection of tasks.
The reducer than compiles the tasks into a single task that can be executed.
At the moment the reducer only supports reducing tasks using the `chain of thought` strategy.

Usage:
    >>> reducer = Reducer()
    >>> reducer.add("step1", func1, param1=1, param2=2)
    >>> reducer.add("step2", func2, param1="step1")
    >>> reducer.add("step3", func3, param1="step2")
    >>> reducer.execute()
    # You can also compile your tasks withouth executing them to review the generated task
    >>> reducer.compile()
"""

from typing import Any

from declarai.tasks.base_llm_task import BaseLLMTask
from declarai import templates


class Reducer:
    def __init__(self):
        self.res = {}

    def add(self, name, func, **kwargs):
        template = templates.InstructFunctionTemplate.format(
            input_instructions=func.llm_translator.parsed_func.doc_description,
            input_placeholder=func.llm_translator.make_input_placeholder(),
            output_instructions=func.llm_translator.make_output_prompt(
                return_name=name
            ),
        )

        llm_task = BaseLLMTask(template=template)
        func.llm_task = llm_task
        self.res[name] = (func, kwargs)

    @staticmethod
    def get_ai_func_template(function, kwargs):
        return function.llm_task.generation_prompt(**kwargs)

    def __compile(self):
        step_count = len(self.res)
        steps = ""
        for step, step_function in enumerate(self.res.values()):
            function, kwargs = step_function
            for k, v in kwargs.items():
                if isinstance(v, tuple) and callable(v[0]):
                    kwargs[k] = "From previous step"
            step_prompt = self.get_ai_func_template(function, kwargs)
            steps += f"Step {step + 1}: {step_prompt}\n"

        ai_func = BaseLLMTask(
            template=templates.ChainOfThoughtsTemplate.format(
                num_steps=step_count,
                steps=steps,
            )
        )
        return ai_func

    def execute(self) -> Any:
        compiled_ai_func = self.__compile()
        res = compiled_ai_func.generate_structured(
            compiled_ai_func.generation_template, multi_results=True
        )
        return res

    def compile(self):
        return self.__compile().generation_template

    def __getitem__(self, item):
        return self.res[item]
