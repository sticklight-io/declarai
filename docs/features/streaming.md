# Streaming

Some LLM providers support streaming of the LLM responses. This is useful when you want to get the results as they are
generated.
In contrast to regular tasks, streaming tasks return a generator that yields the results as they are generated.

## Streaming example

```py
from declarai import Declarai

declarai = Declarai(
    provider="openai",
    model="gpt-3.5-turbo"
)


@declarai.task(streaming=True)  # (1)!
def say_something_about_movie(movie: str) -> str:
    """
    Say something short about the following movie
    :param movie: The movie name
    """

    return declarai.magic(movie)


res = say_something_about_movie(movie="Avengers")

for chunk in res:
    print(chunk.response)

"Av"
"Avengers"
"Avengers is"
"Avengers is an"
"Avengers is an action"
"Avengers is an action-packed"
"Avengers is an action-packed superhero"
"Avengers is an action-packed superhero extrav"
"Avengers is an action-packed superhero extravagan"
"Avengers is an action-packed superhero extravaganza"
"Avengers is an action-packed superhero extravaganza that"
"Avengers is an action-packed superhero extravaganza that brings"
"Avengers is an action-packed superhero extravaganza that brings together"
"Avengers is an action-packed superhero extravaganza that brings together Earth"
"Avengers is an action-packed superhero extravaganza that brings together Earth's"
"Avengers is an action-packed superhero extravaganza that brings together Earth's might"
"Avengers is an action-packed superhero extravaganza that brings together Earth's mightiest"
"Avengers is an action-packed superhero extravaganza that brings together Earth's mightiest heroes"
"Avengers is an action-packed superhero extravaganza that brings together Earth's mightiest heroes to"
"Avengers is an action-packed superhero extravaganza that brings together Earth's mightiest heroes to save"
"Avengers is an action-packed superhero extravaganza that brings together Earth's mightiest heroes to save the"
"Avengers is an action-packed superhero extravaganza that brings together Earth's mightiest heroes to save the world"
"Avengers is an action-packed superhero extravaganza that brings together Earth's mightiest heroes to save the world."
"Avengers is an action-packed superhero extravaganza that brings together Earth's mightiest heroes to save the world."
```

1. Set the `streaming` flag to `True` when defining the task

.
Currently only **OpenAI** & **Azure OpenAI** support streaming.

## Turn on streaming

In order to turn on streaming, you need to set the `streaming` flag to `True` when defining the task.

```py
from declarai import Declarai

declarai = Declarai(
    provider="openai",
    model="gpt-3.5-turbo"
)


@declarai.task(streaming=True)
def my_task()
    ...


@declarai.experimental.chat(streaming=True)
class MyChat
    ...

```

You can also enable streaming globally by settings `stream=True` when initializing the `Declarai` object.

```py
from declarai import Declarai

openai_declarai = Declarai(
    provider="openai",
    model="gpt-3.5-turbo",
    stream=True
)

azure_declarai = Declarai(
    provider="azure",
    model="gpt-3.5-turbo",
    stream=True
)
```

## Accessing the results

The results are returned as a generator. You can iterate over the generator to get the results.

```py
from declarai import Declarai

declarai = Declarai(
    provider="openai",
    model="gpt-3.5-turbo"
)


@declarai.task(streaming=True)
def say_something_about_movie(movie: str) -> str:
    """
    Say something short about the following movie
    :param movie: The movie name
    """

    return declarai.magic(movie)


res_stream = say_something_about_movie(movie="Avengers")

type(res_stream)  # <class 'generator'>

for chunk in res_stream:
    type(chunk)  # <class 'declarai.operators.llm.LLMResponse'>
```

The responses are also saved on the task object.

```py
from declarai import Declarai

declarai = Declarai(
    provider="openai",
    model="gpt-3.5-turbo"
)


@declarai.task(streaming=True)
def say_something_about_movie(movie: str) -> str:
    """
    Say something short about the following movie
    :param movie: The movie name
    """

    return declarai.magic(movie)


res_stream = say_something_about_movie(movie="Avengers")

say_something_about_movie.llm_response  # Empty unless you call next on the generator

say_something_about_movie.llm_stream_response  # <generator object BaseTask.stream_handler at ...> 
```

## Access the delta of the response

You can access the delta of the response by accessing the `raw_response` attribute of the `LLMResponse` object.

The delta is the difference between the current response and the previous response.

This is particularly useful when you want to stream the response to a chatbot, and there is no need to send the entire
response all over again and again.

```py


```py
from declarai import Declarai

declarai = Declarai(
    provider="openai",
    model="gpt-3.5-turbo",
    stream=True
)


@declarai.task
def say_something_about_movie(movie: str) -> str:
    """
    Say something short about the following movie
    :param movie: The movie name
    """

    return declarai.magic(movie)


stream_res = say_something_about_movie("Avengers")

for chunk in stream_res:
    print(chunk.raw_response["choices"][0]["delta"])

# Output
{'role': 'assistant', 'content': ''}
{'content': '"'}
{'content': 'Av'}
{'content': 'engers'}
{'content': ' is'}
{'content': ' an'}
{'content': ' action'}
{'content': '-packed'}
{'content': ' superhero'}
{'content': ' extrav'}
{'content': 'agan'}
{'content': 'za'}
{'content': ' that'}
{'content': ' brings'}
{'content': ' together'}
{'content': ' Earth'}
{'content': "'s"}
{'content': ' might'}
{'content': 'iest'}
{'content': ' heroes'}
{'content': ' to'}
{'content': ' save'}
{'content': ' the'}
{'content': ' world'}
{'content': '."'}
{}
```
