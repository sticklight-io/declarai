"""Reducer

The reducer allows chaining together a collection of tasks.
The reducer than compiles the tasks into a single task that can be executed.
At the moment the reducer only supports reducing tasks using the `chain of thought` strategy.

Usage:
    >>> reducer = Sequence()
    >>> reducer.add("step1", func1, param1=1, param2=2)
    >>> reducer.add("step2", func2, param1="step1")
    >>> reducer.add("step3", func3, param1="step2")
    >>> reducer.execute()
    # You can also compile your tasks withouth executing them to review the generated task
    >>> reducer.compile()
"""

from typing import Literal, Tuple, Set

from declarai import templates
from declarai.tasks.base_llm_task import BaseLLMTask, LLMTaskFuture

ReduceStrategies = Literal["CoT"]


class Sequence:
    def __init__(
        self,
        ai_future_task: LLMTaskFuture,
        reduce_strategy: ReduceStrategies | None = 'CoT'
    ):
        """

        :param ai_future_task: A result to calling `.plan(...)` on a declarai task
        :param reduce_strategy: The strategy to use for reducing the tasks
        """
        self.ai_future_task = ai_future_task
        self.reduce_strategy = reduce_strategy

    @staticmethod
    def reduce_cot(future_task: LLMTaskFuture, prompt: str = "", steps: int = 0, visited_tasks: Set = None) -> Tuple[str, int]:
        if not visited_tasks:
            visited_tasks = set()
        kwargs = future_task.get_kwargs()
        for param, value in kwargs.items():
            if isinstance(value, LLMTaskFuture):
                if value in visited_tasks:
                    kwargs[param] = "From previous steps"
                    continue
                visited_tasks.add(value)
                kwargs[param] = "From previous steps"
                new_prompt, steps = Sequence.reduce_cot(value, prompt, steps, visited_tasks)
                prompt += new_prompt
        steps += 1
        task_prompt = f"Step {steps}:\n{future_task.get_compiled_template().format(**kwargs)}"
        prompt += task_prompt
        return prompt, steps

    def exec(self):
        """
        Executes the task
        :return: The result of the task
        """
        if self.reduce_strategy == "CoT":
            return self.reduce_cot(self.ai_future_task)
        # for k, v in self.ai_future_task.get_kwargs().items():
        #     if isinstance(v, LLMTaskFuture):
        #         self.ai_future_task.kwargs[k] = v()
