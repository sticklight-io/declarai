import importlib
from time import time

from declarai.middlewares.base import TaskMiddleware


class WandDBMonitorCreator:
    """
    Creates a WandDBMonitor middleware for a given task.
    Usage:

    >>> WandDBMonitor = WandDBMonitorCreator(
    ...     name="<task name>",
    ...     project="<project name>",
    ...     key="<decorators-key>",
    ... )
    ...
    >>> @declarai.task(middlewares=[WandDBMonitor])
    ... def generate_a_poem(title: str):
    ...     '''
    ...     Generate a poem based on the given title
    ...     :return: The generated poem
    ...     '''
    ...     return declarai.magic("poem", title)
    """

    def __new__(cls, name: str, project: str, key: str) -> "WandDBMonitor":
        if importlib.util.find_spec("wandb"):
            import wandb
            from wandb.sdk.data_types.trace_tree import Trace

            wandb.login(key=key)
            wandb.init(id=name, name=name, project=project, resume="allow")
        else:
            raise ImportError("wandb is not installed")

        class WandDBMonitor(TaskMiddleware):
            _start_time_ms: time = None

            def before(self, _):
                self._start_time_ms = int(time() / 1000)

            def after(self, task):
                status = "success"
                status_message = ""
                end_time_ms = int(time() / 1000)  # logged in milliseconds
                root_span = Trace(
                    name=task.__name__,
                    kind="llms",
                    status_code=status,
                    status_message=status_message,
                    metadata={
                        "structured": task.prompt_config.structured,
                        "multi_results": task.prompt_config.multi_results,
                        "return_name": task.prompt_config.return_name,
                        "temperature": task.prompt_config.temperature,
                        "max_tokens": task.prompt_config.max_tokens,
                        "top_p": task.prompt_config.top_p,
                        "frequency_penalty": task.prompt_config.frequency_penalty,
                        "presence_penalty": task.prompt_config.presence_penalty,
                        "response": task.llm_response.response,
                        "model": task.llm.model,
                        "prompt_tokens": task.llm_response.prompt_tokens,
                        "completion_tokens": task.llm_response.completion_tokens,
                        "total_tokens": task.llm_response.total_tokens,
                    },
                    start_time_ms=self._start_time_ms,
                    end_time_ms=end_time_ms,
                    inputs={"query": task.compile(**task.call_kwargs)},
                    outputs={"response": task.llm_response.response},
                )

                # log the span to wandb
                root_span.log(name=task.__name__)

        return WandDBMonitor
