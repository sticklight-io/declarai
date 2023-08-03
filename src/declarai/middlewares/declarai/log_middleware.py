import logging
from time import time

from declarai.middlewares.base import TaskMiddleware
from declarai.orchestrator.types import LLMTaskOrchestratorType

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

    def after(self, task: LLMTaskOrchestratorType):
        end_time = time() - self.start_time
        log_record = {
            "task_name": task.__name__,
            "llm_model": task.llm_response.model,
            "template": str(task.compile()),
            "call_kwargs": str(task._kwargs),
            "compiled_template": str(task.compile(**task._kwargs)),
            "result": task.llm_response.response,
            "time": end_time,
        }
        logger.info(log_record)
