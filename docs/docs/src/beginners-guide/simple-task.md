---
hide:
  - footer
---

# Simple task :material-flash:
The simplest Declarai usage is a function decorated with `@declarai.task`:

```py
from declarai import Declarai

declarai = Declarai(provider="openai", model="gpt-3.5-turbo")

@declarai.task
def say_something() -> str:
    """
    Say something short to the world
    """

print(say_something())

> "Spread love and kindness to make the world a better place."
```
In **Declarai**, The docstring represents the task's description and is used to generate the prompt.

By explaining what you want the task to do, the model will be able to understand it and reply with the proper result.



<div style="text-align: right">
    <a href="../controlling-task-behavior" class="md-button">
        Next <i class="fas fa-arrow-right"></i>
    </a>
</div>


