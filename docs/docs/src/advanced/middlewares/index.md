# Middlewares

Middlewares are functions that are executed before or after a task is processed. 
In Declarai, middlewares are used to extend the functionality of tasks, for simple things like monitoring and logging, 
or more complex things like interfering with the task and injecting guardrails into the prompt.


## Creating a middleware

A middleware is a Class that implements a `before` and/or `after` method.
Each accepts a LLMTask object as an argument, and doesn't return anything.


Lets take for exmample this simple implementation of a logging middleware:

```python
import logging
from time import time

from declarai.middlewares.types import TaskMiddleware
from declarai.tasks.types import LLMTaskType

logger = logging.getLogger("LLMLogger")


class LoggingMiddleware(TaskMiddleware):
    start_time: time = None

    def before(self, _):  # (1)!
        self.start_time = time()

    def after(self, task: LLMTaskType):  # (2)!
        end_time = time() - self.start_time
        log_message = f"{task.__name__} took {end_time} seconds to complete"
        logger.info(log_message)
        logger.debug(f"Task results: {task.result}")
```

1. We don't need the task object in the `before` method, so we can ignore it.
2. The after method is called after the task is processed, so we can use the task object to get the task results.


Now all we need to do to use our new middleware is pass it to the `@declarai.task` decorator:

```python
@declarai.task(middlewares=[LoggingMiddleware]) # (1)!
def say_something() -> str:
    """
    Say something short to the world
    """
```

1. We pass the middleware class to the `middlewares` argument of the `@declarai.task` decorator.
