# Magic

The Magic callable is an "empty" function that can be used for two main scenarios:

 - A placeholder for typing, so to simplify interaction with static typing without hacing to mark all Declarai functions with `# type: ignore`:
 - A replacement for the docstring content, if for some reason you don't want to use the docstring for the task description.


### Magic as a placeholder for typing

Without magic:
```python
@openai.task
def suggest_nickname(real_name: str) -> str: # (1)!
    """
    Suggest a nickname for a person
    :param real_name: The person's real name
    :return: A nickname for the person
    """
```

1. type hinter warning on unused argument `real_name` in function.

with magic:
```python
@openai.task
def suggest_nickname(real_name: str) -> str:
    """
    Suggest a nickname for a person
    :param real_name: The person's real name
    :return: A nickname for the person
    """
    return declarai.magic(real_name=real_name) # (1)!
```

1. type hint warning is resolved.


### Replacement for docstring

In the scenario that you do not wan't to rely on the docstring for prompt generation, you can use the magic function to provide the description and parameters.

```python
import declarai

gpt_35 = declarai.openai(model="gpt-3.5-turbo")

@gpt_35.task
def suggest_nickname(real_name: str) -> str:
    return declarai.magic(
        real_name=real_name,
        description="Suggest a nickname for a person",
        params={"real_name": "The person's real name"},
        returns="A nickname for the person",
    )
```

This does take some of Declarai's magic out of the equation, but the result should be all the same.
