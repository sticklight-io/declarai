"""
Logger Middleware
"""
import logging
from time import time

from declarai._base import TaskType
from declarai.middleware.base import TaskMiddleware

logger = logging.getLogger("PromptLogger")


class LoggingMiddleware(TaskMiddleware):
    """
    Creates a Simple logging middleware for a given task.

    Example:
        ```py
        @openai.task(middlewares=[LoggingMiddleware])
        def generate_a_poem(title: str):
            '''
            Generate a poem based on the given title
            :return: The generated poem
            '''
            return declarai.magic("poem", title)
        ```
    """

    start_time: time = None

    def before(self, _):
        """
        Before execution of the task, set the start time.
        """
        self.start_time = time()

    def after(self, task: TaskType):
        """
        After execution of the task, log the task details.
        Args:
            task: the task to be logged

        Returns:
            (Dict[str, Any]): the task details like execution time, task name, template, compiled template, result, time.

        """
        end_time = time() - self.start_time
        log_record = {
            "task_name": task.__name__,
            "llm_model": task.llm_response.model,
            "template": str(task.compile()),
            "call_kwargs": str(self._kwargs),
            "compiled_template": str(task.compile(**self._kwargs)),
            "result": task.llm_response.response,
            "time": end_time,
        }
        logger.info(log_record)
        print(log_record)
