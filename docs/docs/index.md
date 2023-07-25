<p align="center">
  <a href="https://vendi-ai.github.io/declarai/"><img src="./img/Logo-declarai.svg" alt="FastAPI"></a>
</p>
<p align="center">
    <em>Declarai, turning Python functions into LLM tasks, easy to use, and production-ready.</em>
</p>

---

## Introduction

Declarai turns your Python functions into LLM tasks, utilizing your function's details, like type hints and docstrings,
to instruct an AI model on what to do.

Designed with a clear focus on developer experience, you simply write Python code as you normally would, and Declarai
handles the rest.

  ```py title="Declarai Example"
  from declarai import init_declarai, magic
  
  task = init_declarai(provider="openai", model="gpt-3.5-turbo")
  
  
  @task
  def generate_a_joke(title: str) -> str:
      """
      Generate a joke based on the given title 
      :param title: the title of the joke
      :return: A joke made up based on the title
      """
      return magic(title) 
  
  
  print(generate_a_joke(title="Spongebob Squarepants"))
  # > Why did Spongebob Squarepants bring a ladder to the Krusty Krab? Because he wanted to reach new heights in his career as a fry cook!
  ```


---

## Why use Declarai?

- **Pythonic Interface to LLM:** - Leverage python expertise instead of working hard crafting prompts.

- **Type-Guided Prompt Engineering:** - Using Python's type annotations, Declarai crafts precise prompts that guide
  LLMs towards the expected output type. This reduces potential misunderstandings and boosts the consistency of AI
  outputs.

- **Contextual Prompts through Docstrings:** - Use function docstrings to provide contextual information to LLMs,
  enhancing their understanding of the task at hand and improving their performance.

- **Automated LLM Task Execution:** - Feeding prompts to the LLM, collecting and processing responses is seamlessly
  automated, reducing boilerplate and focusing on core application logic.

This approach enhances code readability, maintainability, and predictability

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

## Declarai Examples

To see Declarai in action, we should:

* Decorate a function with the `@task` decorator
* Fill in the `docstrings`
* Make sure to set `type hints` for the function's parameters and return type.

<br>

#### Extract Phone Numbers

In this example, we define a task to extract phone numbers from a given email content.

```py title="extract_phone_number.py" 
from declarai import init_declarai, magic
from typing import List

task = init_declarai(provider="openai", model="gpt-3.5-turbo")


@task # (1)!
def extract_phone_number(email: str) -> List[str] # (2)!
    """
    Extract the phone numbers from the provided email
    :param email: email content
    :return: The phone numbers that are used in the email
    """ # (3)!
    return magic(email)


res = extract_phone_number(
    email="Hello, my phone number is 123456789. What's yours?"
)

print(f"Phone numbers: {res}")
```

1. The `@task` decorator marks the function as a Declarai prompt task.
2. The type hints `List[str]` is used to aprse the output of the llm into a list of strings.
3. The docstring represents the task's description which is used to generate the prompt.

    - `description` - the context of the task
    - `:param` - The function's parameters and their description
    - `:return` - The output description
    

You can run the python script:

<div class="termy">

    ```console
    $ python extract_phone_number.py
    
    Phone numbers: [123456789]
    ```

</div>

<br>

#### Search blog posts

In this example, we define a semantic search for relevant blog posts based on a given query.

```Python title="search_blog_posts.py"
from declarai import init_declarai, magic, VectorStore
from typing import List

search = init_declarai(provider="openai", model="text-embedding-ada-002")


@search # (1)!
def get_relevant_blog_posts(query: str, data: VectorStore) -> List[str]:
  """
  Find the relevant blog posts
  :param query: A use provided query to search with
  :param data: A vector store data object that contains the blog posts
  :return: The relevant blog posts
  """
  return magic(query, data)


blogs_posts = get_relevant_blog_posts(
  "What can I do with Declarai?",
  VectorStore.from_csv("blog_posts.csv")
)

print(f"Blog posts: {blogs_posts}")
#> Blog posts: ['How to use Declarai?', 'How to use Declarai in production?']
```

1. The `@search` decorator marks the function as a Declarai semantic search task.
2. 
<br>

### Multitask flow

We can leverage Chain-of-thought to efficiently solve multiple tasks in a single flow.
```Python title="sequence_of_tasks.py"

from declarai import Sequence, init_declarai, magic

task = init_declarai(provider="openai", model="gpt-3.5-turbo")


@task
def suggest_title(question: str) -> str:
  """
  Given a question from our customer support, suggest a title for it
  :param question: the provided question
  :return: The title suggested for the question
  """
  return magic(question)


@task
def route_to_department(title: str, departments: List[str]) -> str:
  """
  Given a question title, route it to the relevant department
  :param title: A title generated for the question
  :param departments: The departments to route the question to
  :return: The department that the question should be routed to
  """
  return magic(title, departments)


@task
def suggest_department_answers(question: str, department: str) -> List[str]:
  """
  Given a question and a department, suggest 2 answers from the department's knowledge base
  :param question: The question to suggest answers for
  :param department: The department to suggest answers from
  :return: The suggested answers
  """
  return magic(question, department)

  
available_departments = ["sales", "support", "billing"]
question = "I have a feature request for your product. Who should I talk to?"

suggested_title = suggest_title.plan(question=question)
selected_department = route_to_department.plan(
  title=suggested_title, departments=available_departments
)
suggested_answers = suggest_department_answers.plan(
  question=question, department=selected_department
)

res = suggested_answers(reduce="CoT")

print(res)
"""
{
    "suggested_answers": ["You can talk to our sales team", "You can talk to our support team"],
    "selected_department": "sales",
    "suggested_title": "Feature request"
}
"""
```




