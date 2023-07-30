<p align="center">
  <a href="https://vendi-ai.github.io/declarai/"><img src="./img/Logo-declarai.svg" alt="FastAPI"></a>
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

- **Lightweight:** - Declarai is written almost solely in python 3.6 with optional SDKs, 
  so there's no need to worry about dependencies.

- **Extendable:** - Declarai is designed to be easily extendable, the interface is simple and accessible by design so
  you can easily override or customize the behavior of the framework to your specific needs.

- **Type-Driven Prompt Design:** - Through the application of Python's type annotations, 
  Declarai constructs detailed prompts that guide Large Language Models (LLMs) to generate the desired output type.

- **Context-Informed Prompts via Docstrings:** - Implement function docstrings to supply contextual data to LLMs, 
  augmenting their comprehension of the designated task and thereby boosting their performance.

- **Automated Execution of LLM Tasks:** - Declarai takes care of the execution code, letting you concentrate on the core business logic.

Utilizing Declarai leads to improved code readability, maintainability, and predictability.

---

## Installation
!!! info
     
     Following is the basic installatoin which comes with no integrations of dependencies except for openai sdk, 
     for a full list of supported extnesions, please view the [integrations](/src/integrations/) page.

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

```py title="Simple Syntax" 

@declarai.task # (1)!
def extract_phone_number(email_content: str) -> List[str]: # (2)!
    """
    Extract the phone numbers from the provided email_content
    :param email_content: Text represents the email content 
    :return: The phone numbers that are used in the email
    """# (3)!
    return declarai.magic(email_content) # (4)!

```

1. The `@declarai.task` decorator marks the function as a Declarai prompt task.
2. The type hints `List[str]` is used to parse the output of the llm into a list of strings.
3. The docstring represents the task's description which is used to generate the prompt.
    - `description` - the context of the task
    - `:param` - The function's parameters and their description
    - `:return` - The output description
4. The `magic` method is an optional placeholder for typing, and can be used as a replacement for the docstring interface when needed.

<br>

#### Task Middlewares
Easy to use middlewares provided out of the box as well as the ability to easily create your own.

```py title="Simple Middleware"

```python
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

<br>

#### Complex Schema handling using pydantic

In this example, we provide pydantic schemas to create meaningful objects for our application

```python title="Schema"
class TimeFrame(BaseModel):
    start: int
    end: int


class BusinessExperience(BaseModel):
    time_frame: TimeFrame
    title: str
    description: str
    company: str


class Recommendation(BaseModel):
    recommender: str
    recommendation: str


class BusinessProfile(BaseModel):
    bio: str
    experience: List[BusinessExperience]
    previous_jobs: List[str]
    recommendations: List[Recommendation]
```
All we need to do is provide the desired schema as the return type of the function
```py title="Complex Schema"
@declarai.task
def generate_business_profile(name: str, skills: List[str]) -> BusinessProfile:
    """
    Generate a business profile based on the given name and skills
    Produce a short bio and a mapping of the skills and where they can be used
    for fields with missing data, you can make up data to fill in the gaps
    :param name: The name of the person
    :param skills: The skills of the person
    :return: The generated business profile
    """
    return declarai.magic(name=name, skills=skills)
```
Usage:
```python title="Business Profile"
profile = generate_business_profile(
    name="Bob grapes",
    skills=[
        "Management", "entrepreneurship", "programming", "investing", "Machine Learning"
    ],
)
print(profile)
```
Shortened to fit the page:
```console
{
    'bio': 'Bob Grapes is a highly skilled professional with expertise in management, 
    entrepreneurship, programming, investing, and machine learning. 
    With a strong background in ... ",
    'experience': [
        {
            'time_frame': {
                'start': 2010, 
                'end': 2015
            }, 
            'title': 'Manager', 
            'description': 'Managed a team of 20 employees and oversaw daily operations', 
            'company': 'ABC Company'
        },
            ... 
        ], 
    'previous_jobs': [
        'ABC Company', 
        'XYZ Startup', 
        'DEF Tech', 
        'GHI Corporation'
    ], 
    'recommendations': [
        {
            'recommender': 'John Smith', 
            'recommendation': 'Bob is an exceptional leader with ..."
        },
        ...
    ]
}
```
 
<br>

### Complex flow optimization

For more complex scenarios,  we may not want to cram too much into a single task. 
This is a classic case of abstraction and separation of concerns.

In order to achieve this, declarai provides a `Sequence` class that allows you to chain multiple tasks together.
These tasks will be reduced to a single prompt that will be executed in a **single call to the llm**.

```python title="Sequence"
@declarai.task
def suggest_title(question: str) -> str:
  """
  Given a question from our customer support, suggest a title for it
  :param question: the provided question
  :return: The title suggested for the question
  """
  return declarai.magic(question)


@declarai.task
def route_to_department(title: str, departments: List[str]) -> str:
  """
  Given a question title, route it to the relevant department
  :param title: A title generated for the question
  :param departments: The departments to route the question to
  :return: The department that the question should be routed to
  """
  return declarai.magic(title, departments)


@declarai.task
def suggest_department_answers(question: str, department: str) -> List[str]:
  """
  Given a question and a department, suggest 2 answers from the department's knowledge base
  :param question: The question to suggest answers for
  :param department: The department to suggest answers from
  :return: The suggested answers
  """
  return declarai.magic(question, department)


# In the following we chain the tasks together to create a single prompt
# The result will:
# - Suggest a title for the question
# - Route the question to the relevant department
# - Suggest 2 answers from the department's knowledge base

def suggest_answers(question: str, available_departments: List[str]) -> Dict[str, Any]:
    suggested_title = suggest_title.plan(question=question)
    selected_department = route_to_department.plan(
      title=suggested_title, departments=available_departments
    )
    suggested_answers = suggest_department_answers.plan(
      question=question, department=selected_department
    )
    return suggested_answers(reduce_strategy="ChainOfThought")
```
Usage:
```python
suggested_answers = suggest_answers(
    question="I want to be able to click on that button but I can't. Is this currently possible?", 
    available_departments=["sales", "support"])
)
print(suggested_answers)
```
```console
{
    "suggested_answers": [
        "This isn't supported at the moment, you are welcome to open a feature request on our website!", 
        "We have accepted you request and will check if this behavior is currently possible. We will get back to you shortly."
    ],
    "selected_department": "support",
    "suggested_title": "Feature request"
}
```
