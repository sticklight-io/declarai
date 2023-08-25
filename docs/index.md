<p align="center">
  <a href="https://vendi-ai.github.io/declarai/"><img src="./img/Logo-declarai.svg" alt="Declarai"></a>
</p>
<p align="center">
    <em>Declarai, turning Python code into LLM tasks, easy to use, and production-ready.</em>
</p>

---

## Introduction

Declarai turns your Python code into LLM tasks, utilizing python's native syntax, like type hints and docstrings,
to instruct an AI model on what to do.

Designed with a clear focus on developer experience, you simply write Python code as you normally would, and Declarai
handles the rest.

  ```py title="poem_generator.py"
  from declarai import Declarai
  
  declarai = Declarai(provider="openai", model="gpt-3.5-turbo")
  
  @declarai.task
  def generate_poem(title: str) -> str:
      """
      Write a 4 line poem on the provided title
      """
  
  
  res = generate_poem(
      title="Declarai, the declarative framework for LLMs"
  )
  print(res)
  ```
  ```console
  >>> Declarai, the AI framework,
  ... Empowers LLMs with declarative power,
  ... Efficiently transforming data and knowledge,
  ... Unlocking insights in every hour.
  ```

---

## Why use Declarai?

- **Pythonic Interface to LLM:** - Leverage your existing Python skills instead of spending unnecessary time creating complex prompts.

- **Lightweight:** - Declarai is written almost solely in python 3.6 using only pydantic and openai SDKs, so there's no need to worry about dependency spaghetti.

- **Extendable:** - Declarai is designed to be easily extendable, the interface is simple and accessible by design so
  you can easily override or customize the behavior of the framework to your specific needs.

- **Type-Driven Prompt Design:** - Through the application of Python's type annotations, 
  Declarai constructs detailed prompts that guide Large Language Models (LLMs) to generate the desired output type.

- **Context-Informed Prompts via Docstrings:** - Implement function docstrings to supply contextual data to LLMs, 
  augmenting their comprehension of the designated task, thereby boosting their performance.

- **Automated Execution of LLM Tasks:** - Declarai takes care of the execution code, letting you concentrate on the core business logic.

Utilizing Declarai leads to improved code readability, maintainability, and predictability.

---

## Installation
<div class="termy">

```console
$ pip install declarai

---> 100%
Done!
```

</div>


---

## Feature highlight

### Python native syntax
Integrating deeply into python's native syntax, declarai understands your code and generates the prompt accordingly.

```python title="Simple Syntax"
@declarai.task # (1)!
def rank_by_severity(message: str) -> int: # (2)!
    """
    Rank the severity of the provided message by it's urgency.
    Urgency is ranked on a scale of 1-5, with 5 being the most urgent.
    :param message: The message to rank
    :return: The urgency of the message
    """ # (3)!


print(rank_by_severity(message="The server is down!"))
#> 5
print(rank_by_severity(message="How was your weekend?"))
#> 1
```

1. The `@declarai.task` decorator marks the function as a Declarai prompt task.
2. The type hints `List[str]` are used to parse the output of the llm into a list of strings.
3. The docstring represents the task's description which is used to generate the prompt.
    - `description` - the context of the task
    - `:param` - The function's parameters and their description
    - `:return` - The output description

    
### Support Python typing and pydantic models
Declarai will return a serialized object as defined by the type hints at runtime.
```py title="Builtins"
@declarai.task
def extract_phone_number(email_content: str) -> List[str]:
    """
    Extract the phone numbers from the provided email_content
    :param email_content: Text that represents the email content 
    :return: The phone numbers that are used in the email
    """

print(extract_phone_number(email_content="Hi, my phone number is 123-456-7890"))
#> ['123-456-7890']
```

```python title="Builtins"
@declarai.task
def datetime_parser(raw_date: str) -> datetime:
    """
    Parse the input into a valid datetime string of the format YYYY-mm-ddThh:mm:ss
    :param raw_date: The provided raw date
    :return: The parsed datetime output
    """


print(datetime_parser(raw_date="Janury 1st 2020"))
#> 2020-01-01 00:00:00
```


```python title="Pydantic models"
class Animal(BaseModel):
    name: str
    family: str
    leg_count: int = Field(description="The number of legs")


@declarai.task
def suggest_animals(location: str) -> Dict[int, List[Animal]]:
    """
    Create a list of numbers from 0 to 5
    for each number, suggest a list of animals with that number of legs
    :param location: The location where the animals can be found
    :return: A list of animal leg count and for each count, the corresponding animals
    """


print(suggest_animals(location="jungle"))
#> {
#       0: [
#           Animal(name='snake', family='reptile', leg_count=0)
#       ], 
#       2: [
#           Animal(name='monkey', family='mammal', leg_count=2), 
#           Animal(name='parrot', family='bird', leg_count=2)
#       ], 
#       4: [
#          Animal(name='tiger', family='mammal', leg_count=4), 
#          Animal(name='elephant', family='mammal', leg_count=4)
#       ]
# }
```
<br>

### Chat interface
Create chat interfaces with ease, simply by writing a class with docstrings

!!! info  
    Notice that `chat` is exposed under the `experimental` namespace, noting this interface is still work in progress.

```python
@declarai.experimental.chat
class CalculatorBot:
    """
    You a calculator bot,
    given a request, you will return the result of the calculation
    """

    def send(self, message: str) -> int: ...


calc_bot = CalculatorBot()
print(calc_bot.send(message="1 + 1"))
#> 2
```
<br>

### Task Middlewares
Easy to use middlewares provided out of the box as well as the ability to easily create your own.

```py title="Logging Middleware"
@declarai.task(middlewares=[LoggingMiddleware])
def extract_info(text: str) -> Dict[str, str]:
    """
    Extract the phone number, name and email from the provided text
    :param text: content to extract the info from
    :return: The info extracted from the text
    """
    return Declarai.magic(text=text)

res = extract_info(
    text="Hey jenny,"
    "you can call me at 124-3435-132."
    "You can also email me at georgia@coolmail.com"
    "Have a great week!"
)
print(res)
``` 
Result:
```console
{'task_name': 'extract_info', 'llm_model': 'gpt-3.5-turbo-0301', 'template': '{input_instructions}\n{input_placeholder}\n{output_instructions}', 'template_args': {'input_instructions': 'Extract the phone number, name and email from the provided text', 'input_placeholder': 'Inputs:\ntext: {text}\n', 'output_instructions': 'The output should be a markdown code snippet formatted in the following schema, including the leading and trailing \'```json\' and \'```\':\n```json\n{{\n    "declarai_result": Dict[str, str]  # The info extracted from the text\n}}\n```'}, 'prompt_config': {'structured': True, 'multi_results': False, 'return_name': 'declarai_result', 'temperature': 0.0, 'max_tokens': 2000, 'top_p': 1.0, 'frequency_penalty': 0, 'presence_penalty': 0}, 'call_kwargs': {'text': 'Hey jenny,you can call me at 124-3435-132.You can also email me at georgia@coolmail.comHave a great week!'}, 'result': {'phone_number': '124-3435-132', 'name': 'jenny', 'email': 'georgia@coolmail.com'}, 'time': 2.192906141281128}
{'phone_number': '124-3435-132', 'name': 'jenny', 'email': 'georgia@coolmail.com'}
```

We highly recommend you to go through the beginner's guide to get a better understanding of the library and its capabilities - [Beginner's Guide](./beginners-guide)

