<p align="center">
  <a href="https://github.com/vendi-ai/declarai">
    <img src="https://img.shields.io/pypi/pyversions/declarai.svg" alt="versions">
  </a>
  <a href="https://github.com/vendi-ai/declarai">
    <img src="https://img.shields.io/github/license/vendi-ai/declarai.svg" alt="license">
  </a>
  <a href="https://github.com/vendi-ai/declarai/actions/workflows/test.yaml">
    <img src="https://github.com/vendi-ai/declarai/actions/workflows/test.yaml/badge.svg" alt="Tests">
  </a>
  <a href="https://pypi.org/project/declarai/">
    <img src="https://img.shields.io/pypi/v/declarai?color=%2334D058&label=pypi%20package" alt="Pypi version">
  </a>
    <a href="https://pepy.tech/project/declarai">
    <img src="https://static.pepy.tech/badge/declarai/month" alt="Pypi downloads">
  </a>
  <a href="https://discord.gg/GrszSXNTDm">
    <img src="https://dcbadge.vercel.app/api/server/GrszSXNTDm?compact=true&style=flat" alt="Discord invite">
  </a>
  <a target="_blank" href="https://colab.research.google.com/github/vendi-ai/declarai/blob/main/examples/declarai_intro.ipynb">
    <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
  </a>
</p>

<p align="center">
  <img src="assets/Logo-declarai.png" alt="Logo - declarai.png">
</p>

---

**Documentation 📖**: <a href="https://vendi-ai.github.io/declarai" target="_blank">https://declarai.com </a>

**Source Code 💻** : <a href="https://github.com/vendi-ai/declarai" target="_blank">https://github.com/vendi-ai/declarai </a>

---

## What is Declarai 🤔?

**Declarai** turns your Python code into LLM tasks, allowing you to easily integrate LLM into your existing codebase.
It operates on a simple principle: just define a Python function/class. 
By annotating this function with docstrings and type hints, you provide a clear instruction set for the AI model without any additional effort.

Once you've declared your function, Declarai intelligently compiles the function's docstrings and type hints into a prompt for the AI model, ensuring the model understands exactly what's required.

After executing the task, Declarai retrieves the AI's response and parses it, translating it back into the declared return type of your Python function. This eliminates any manual parsing or post-processing on your part.

**Declarai** Keeps It Native: At its core, Declarai is about embracing native Python practices. You don't need to learn a new syntax or adapt to a different coding paradigm. Just write Python functions as you always have, and let Declarai handle the AI integration seamlessly.

---
## Main Components 🧩

### Tasks 💡

AI tasks are used for any business logic or transformation.
```python
import declarai

gpt_35 = declarai.openai(model="gpt-3.5-turbo")

@gpt_35.task 
def rank_by_severity(message: str) -> int:
    """
    Rank the severity of the provided message by it's urgency.
    Urgency is ranked on a scale of 1-5, with 5 being the most urgent.
    :param message: The message to rank
    :return: The urgency of the message
    """


rank_by_severity(message="The server is down!")

>>> 5

rank_by_severity(message="How was your weekend?"))

>>> 1
```
### Chat 🗣

AI Chats are used for an iterative conversation with the AI model, where the AI model can remember previous messages and context.

```python
import declarai

gpt_35 = declarai.openai(model="gpt-3.5-turbo")

@gpt_35.experimental.chat
class SQLBot:
    """
    You are a sql assistant. You help with SQL related questions 
    """


sql_bot = SQLBot()
sql_bot.send("When should I use a LEFT JOIN?")

> "You should use a LEFT JOIN when you want to return all rows from ....
```

 
### Features:

- [x] 🖍 **Intelligent Prompts**: Automatically generate prompts using type hints and docstrings.
- [x] 🚄 **Conversational AI**: Chat interface equipped with memory and context management.
- [x] ⚡ **Real-time streaming**: Stream LLM responses that take longer to complete.
- [x] 🔥 **Pydantic Model Parsing**: Seamlessly parse llm responses into[ Pydantic models](https://github.com/vendi-ai/declarai#pydantic-models).
- [x] 🐍 **Pythonic**: Native understanding and parsing of llm responses into [Python primitives](https://github.com/vendi-ai/declarai#tasks-with-python-native-output-parsing).
- [x] 💾 **Multiple AI Backends**: Integrated with OpenAI & Azure AI llm providers.
- [x] 🛠 **Middleware**: Adapt and extend tasks behavior with a modular middleware system.
- [ ] 🤗 **Coming Soon**: Integration with HuggingFace hub

## Quickstart 🚀

### Installation
```bash
pip install declarai
```

### Setup
```bash
export OPENAI_API_KEY=<your openai token>
```
or pass the token when initializing the declarai object
```python
import declarai

gpt_35 = declarai.openai(model="gpt-3.5-turbo", openai_token="<your-openai-key>")
```

## 💡 Basic Usage
Craft AI-powered functionalities with ease using the `@task` decorator. Just add some type hints and a bit of documentation, and watch Declarai do its magic!
```python
import declarai

gpt_35 = declarai.openai(model="gpt-3.5-turbo")

@gpt_35.task
def generate_poem(title: str) -> str:
    """
    Write a 4 line poem on the provided title
    """


res = generate_poem(
    title="Declarai, the declarative AI framework for LLMs"
)
print(res)
# Declarai, the AI framework,
# Empowers LLMs with declarative power,
# Efficiently transforming data and knowledge,
# Unlocking insights in every hour.
```
Not the best poem out there, but hey! You've written your first declarative AI code!

Declarai aims to promote clean and readable code by enforcing the use of doc-strings and typing.
The resulting code is readable and easily maintainable.


### Tasks with python native output parsing

Python primitives
```python
import declarai

gpt_35 = declarai.openai(model="gpt-3.5-turbo")

@gpt_35.task
def rank_by_severity(message: str) -> int:
    """
    Rank the severity of the provided message by it's urgency.
    Urgency is ranked on a scale of 1-5, with 5 being the most urgent.
    :param message: The message to rank
    :return: The urgency of the message
    """


rank_by_severity(message="The server is down!")

>>> 5
rank_by_severity(message="How was your weekend?"))

>>> 1
```
Python Lists/Dicts etc..

```python
from typing import List
import declarai

gpt_35 = declarai.openai(model="gpt-3.5-turbo")

@gpt_35.task
def multi_value_extraction(text: str) -> List[str]:
    """
    Extract the phone numbers from the provided text
    :param text: content to extract phone number from
    :return: The phone numbers that where identified in the input text
    """


multi_value_extraction(
    text="Hey jenny,\nyou can call me at 124-3435-132.\n"
         "you can also reach me at +43-938-243-223"
)
>>> ['124-3435-132', '+43-938-243-223']
```
Python complex objects
```python
from datetime import datetime
import declarai

gpt_35 = declarai.openai(model="gpt-3.5-turbo")

@gpt_35.task
def datetime_parser(raw_date: str) -> datetime:
    """
    Parse the input into a valid datetime string of the format YYYY-mm-ddThh:mm:ss
    :param raw_date: The provided raw date
    :return: The parsed datetime output
    """


datetime_parser(raw_date="Janury 1st 2020"))

>>> 2020-01-01 00:00:00
```

### Pydantic models
```python
from pydantic import BaseModel
from typing import List, Dict
import declarai


class Animal(BaseModel):
    name: str
    family: str
    leg_count: int

gpt_35 = declarai.openai(model="gpt-3.5-turbo")

@gpt_35.task
def suggest_animals(location: str) -> Dict[int, List[Animal]]:
    """
    Create a list of numbers from 0 to 5
    for each number, suggest a list of animals with that number of legs
    :param location: The location where the animals can be found
    :return: A list of animal leg count and for each count, the corresponding animals
    """


suggest_animals(location="jungle")

>>> {
       0: [
           Animal(name='snake', family='reptile', leg_count=0)
       ], 
       2: [
           Animal(name='monkey', family='mammal', leg_count=2), 
           Animal(name='parrot', family='bird', leg_count=2)
       ], 
       4: [
          Animal(name='tiger', family='mammal', leg_count=4), 
          Animal(name='elephant', family='mammal', leg_count=4)
       ]
 }
```
### Jinja templates 🥷
```python
import declarai

gpt_35 = declarai.openai(model="gpt-3.5-turbo")

@gpt_35.task
def sentiment_classification(string: str, examples: List[str, int]) -> int:
    """
    Classify the sentiment of the provided string, based on the provided examples.
    The sentiment is ranked on a scale of 1-5, with 5 being the most positive.
    {% for example in examples %}
    {{ example[0] }} // {{ example[1] }}
    {% endfor %}
    {{ string }} //
    """
    
sentiment_classification(string="I love this product but there are some annoying bugs",
                         examples=[["I love this product", 5], ["I hate this product", 1]])

>>> 4
```

### Simple Chat interface

```python
import declarai

gpt_35 = declarai.openai(model="gpt-3.5-turbo")

@gpt_35.experimental.chat
class CalculatorBot:
    """
    You a calculator bot,
    given a request, you will return the result of the calculation
    """

    def send(self, message: str) -> int: ...


calc_bot = CalculatorBot()
calc_bot.send(message="1 + 1")

>>> 2
```


📚 For a thorough introduction, features, and best practices, explore our [official documentation](https://vendi-ai.github.io/declarai/) and [beginner's guide](https://vendi-ai.github.io/declarai/beginners-guide/).

## Contributing 💼
Join our mission to make declarative AI even better together! Check out our [contributing guide](https://vendi-ai.github.io/declarai/contribute/) to get started.

