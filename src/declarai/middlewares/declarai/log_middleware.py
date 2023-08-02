import logging
from time import time

from declarai.middlewares.types import TaskMiddleware
from declarai.tasks.types import LLMTaskType

logger = logging.getLogger("PromptLogger")


class LoggingMiddleware(TaskMiddleware):
    """
    Creates a Simple logging middleware for a given task.
    Usage:
    >>> @declarai.task(middlewares=[LoggingMiddleware])
    ... def generate_a_poem(title: str):
    ...     '''
    ...     Generate a poem based on the given title
    ...     :return: The generated poem
    ...     '''
    ...     return declarai.magic("poem", title)
    """

    start_time: time = None

    def before(self, _):
        self.start_time = time()

    def after(self, task: LLMTaskType):
        end_time = time() - self.start_time
        log_record = {
            "task_name": task.__name__,
            "llm_model": task.llm.model,
            "template": task.template,
            "template_args": task.template_args,
            "prompt_config": task.prompt_config.__dict__,
            "call_kwargs": task.call_kwargs,
            "result": task.result,
            "time": end_time,
        }
        logger.warning(log_record)
