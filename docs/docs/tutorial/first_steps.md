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


## Passing parameters to the task  :accordion:
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


## Declare response :outbox_tray:

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

!!! tip 
    You are free to use any description you want in the docstring.

    The better you describe the task, :params and :return sections within the docstring, the better the results will be.


## Compile task
Once you have defined your task, you can compile it if you want to view the prompt that will be used to generate the results.

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


say_something_about_movie.compile()
> """
Say one thing you liked and one thing you didn't like about the following movie
Inputs:
movie: {movie}
The output should be a markdown code snippet formatted in the following schema, including the leading and trailing '```json' and '```':
```json
{{
    result: typing.List[str]  #  A list of two strings - one thing you liked and one thing you didn't like
}}
"""
```
You can see that the real prompt sent to the model is a bit different than the docstring.

Declarai uses the docstring to generate the prompt, but it also adds some minimal additional information to the prompt, helping the model to generate better results.
You can also compile the task with the real values of the parameters:

You can also compile the task with the real values of the parameters:

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

say_something_about_movie.compile(movie="Avengers")
>"""
Say one thing you liked and one thing you didn't like about the following movie
Inputs:
movie: Avengers 
The output should be a markdown code snippet formatted in the following schema, including the leading and trailing '```json' and '```':
```json
{{
    result: typing.List[str]  #  A list of two strings - one thing you liked and one thing you didn't like
}}
""" # (1)!
```

1. The real value `movie="Avengers"` is added to the prompt.

!!! tip 
    You can use the `compile` method to view the prompt that will be sent to the model.

    You can also use the `compile` method to view the prompt with the real values of the parameters.

    This can be useful when you want to debug your task.

## Plan task :material-airplane-clock:
Once you have defined your task, you can create a plan for it that is already populated with the real values of the parameters.

The plan is an object you call and get the results. This is very helpful when you want to populate the task with the real values of the parameters but delay the execution of it. 
    
```py

from declarai import init_declarai, magic

task = init_declarai(provider="openai", model="gpt-3.5-turbo")

@task
def say_something_about_movie(movie: str) -> str:  
    """
    Say something short about the following movie
    :param movie: The movie name
    """

    return magic(movie)

plan = say_something_about_movie.plan(movie="Avengers")

print(plan)
> #<declarai.tasks.base_llm_task.LLMTaskFuture object at 0x106795790>


print(plan.get_populated_prompt())
>"""
Say one thing you liked and one thing you didn't like about the following movie
Inputs:
movie: Avengers 
The output should be a markdown code snippet formatted in the following schema, including the leading and trailing '```json' and '```':
```json
{{
    result: typing.List[str]  #  A list of two strings - one thing you liked and one thing you didn't like
}}
"""

# Execute the task by calling the plan
plan()
> ['I liked the action-packed storyline and the epic battle scenes.',
   "I didn't like the lack of character development for some of the Avengers."]
```


!!! warning "Important"
    The plan is an object you call and get the results. This is very helpful when you want to populate the task with the real values of the parameters but delay the execution of it.
    If you just want to execute the task, you can call the task directly.

    ```py
    res = say_something_about_movie(movie="Avengers")

    > ['I liked the action-packed storyline and the epic battle scenes.',
    "I didn't like the lack of character development for some of the Avengers."]
    ```
 
## Recap
- Create a declarai task.
- Add type hints to the task.
- Add a docstring to the task.
- Use the `compile` method to view the prompt that will be sent to the model.
- Use the 'plan' method to create a plan for the task.



