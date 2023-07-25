## Simple task :material-flash:
The simplest Declarai usage is a function decorated with `@task`:

```py
from declarai import init_declarai, magic

task = init_declarai(provider="openai", model="gpt-3.5-turbo")

@task
def say_something() -> str:
    """
    Say something short to the world
    """
    return magic()

print(say_something())

> "Spread love, kindness, and unity."
```
In **Declarai**, The docstring represents the task's description which is used to generate the prompt.
    
   - `description` - the context of the task
   - `:param` - The function's parameters and their description
   - `:return` - The output description

In the example about we have created a task called `say_something` that returns a string.
The task is using the `openai` provider, and the `gpt-3.5-turbo` model.
When we call the task, it will use the model to generate a string for us by following the task's docstring.


## Passing parameters to the task
Here we declare a task that takes a `movie` parameter and returns a string.

We use the `:param` fields in docstrings to describe the task's parameters.
```py
from declarai import init_declarai, magic

task = init_declarai(provider="openai", model="gpt-3.5-turbo")

@task
def say_something_about_movie(movie: str) -> str:  # (1)!
    """
    Say something short about the following movie
    :param movie: The movie name
    """
    
    return magic(movie)

print(say_something_about_movie(movie="Avengers"))

> """The Avengers is an action-packed superhero movie featuring a team of 
powerful and charismatic characters"""
```

1. The `movie` parameter is a string.  Don't forget to add type hints to your task

!!! note "Type hints"
    Please use type hints to describe the input and output of the task.


## Declare response 

Here we declare a task that returns a list of strings.

Using `:return` in docstrings we can describe the output of the task.
 
By declaring the output type, we make sure that the output of the model will be parsed to the provided type.

```py
from declarai import init_declarai, magic
from typing import List

task = init_declarai(provider="openai", model="gpt-3.5-turbo")


@task
def say_something_about_movie(movie: str) -> List[str]: # (1)!
    """
    Say one thing you liked and one thing you didn't like about the following movie
    :param movie: The movie name
    :return: A list of two strings - one thing you liked and one thing you didn't like 
    """

    return magic(movie)


print(say_something_about_movie(movie="Avengers"))

> ['I liked the action-packed storyline and the epic battle scenes.',
   "I didn't like the lack of character development for some of the Avengers."]

```

1. The `say_something_about_movie` task returns a list of strings.  Don't forget to add type hints to your task

??? note "Quality of the results"
    The better you describe the task and the :param & :return, the better the results will be.



