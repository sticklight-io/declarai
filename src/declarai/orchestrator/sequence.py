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

from typing import Optional, Set, Tuple

from typing_extensions import Literal

from declarai.operators.shared import templates
from declarai.orchestrator.future_llm_task import FutureLLMTask

ReduceStrategies = Literal["ChainOfThought"]


class Sequence:
    def __init__(
        self,
        ai_future_task: FutureLLMTask,
        reduce_strategy: Optional[ReduceStrategies] = "ChainOfThought",
    ):
        """

        :param ai_future_task: A result to calling `.plan(...)` on a declarai task
        :param reduce_strategy: The strategy to use for reducing the tasks
        """
        self.ai_future_task = ai_future_task
        self.reduce_strategy = reduce_strategy

    def _exec(self):
        """
        Executes the task
        :return: The result of the task
        """
        if self.reduce_strategy == "ChainOfThought":
            prompt, num_steps = chain_of_thought_reducer(self.ai_future_task)
            reduced_prompt = templates.ChainOfThoughtsTemplate.format(
                steps=prompt, num_steps=num_steps
            )
            self.ai_future_task.exec_func.__self__.prompt_config.multi_results = True
            return self.ai_future_task.exec_func(reduced_prompt)

    def __call__(self):
        return self._exec()


def chain_of_thought_reducer(
    future_task: FutureLLMTask,
    prompt: str = "",
    steps: int = 0,
    visited_tasks: Set = None,
) -> Tuple[str, int]:
    """
    Recursive resolving of future_ai_tasks
    and compiling them into a single task with the chain of thought strategy.
    """
    if not visited_tasks:
        visited_tasks = set()

    kwargs = future_task.task_kwargs

    for param, value in kwargs.items():
        if isinstance(value, FutureLLMTask):
            if value not in visited_tasks:
                visited_tasks.add(value)
                new_prompt, new_steps = chain_of_thought_reducer(
                    value, "", steps, visited_tasks
                )
                prompt += new_prompt
                steps = new_steps
            kwargs[param] = "From previous steps"

    steps += 1
    task_prompt = f"\nStep {steps}:\n{future_task.compiled_template.format(**kwargs)}"
    prompt += task_prompt
    return prompt, steps
