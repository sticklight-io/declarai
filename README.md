# Introducing declareai

![Logo - declarai.png](assets/Logo-declarai.png)

Using AI in your code shouldn't be difficult. Supporting the mission of bringing AI to the masses,
this repo is meant to abstract the know-how of prompt engineering and make using LLMs for daily programming accessible to everyone.

If you know how to write python code and have written any doc-string in your life, this should be a breeze.

## Installation
```bash
pip install declarai
```

## Setup
```bash
export USE_AI_OPENAI_TOKEN= <your openai token>
```

## Usage:
The most basic functionality. Just add the `@task` decorator to your function, add some documentation and you're good to go!
```python
from declarai import Declarai

declarai = Declarai(provider="openai", model="gpt-3.5-turbo")

@declarai.task
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

For more complex use cases you can use a reducer, to build and compile multiple prompts into one!

```python
from typing import Any, Dict, List
from declarai import Declarai, Sequence

ALL_DEPARTMENTS = ["sales", "support", "billing"]

declarai = Declarai(provider="openai", model="gpt-3.5-turbo")


@declarai.task
def suggest_title(question: str) -> str:
    """
    Given a question from our customer support, suggest a title for it
    :param question: the provided question
    :return: The title suggested for the question
    """
    return declarai.magic("question_title", question=question)


@declarai.task
def route_to_department(title: str, departments: List[str]) -> str:
    """
    Given a question title, route it to the relevant department
    :param title: A title generated for the question
    :param departments: The departments to route the question to
    :return: The department that the question should be routed to
    """
    return declarai.magic("department", title=title, departments=departments)


@declarai.task
def suggest_department_answers(question: str, department: str) -> List[str]:
    """
    Given a question and a department, suggest 2 answers from the department's knowledge base
    :param question: The question to suggest answers for
    :param department: The department to suggest answers from
    :return: The suggested answers
    """
    return declarai.magic("answers", question=question, department=department)


def handle_customer_question(question: str) -> Dict[str, Any]:
    suggested_title = suggest_title.plan(question=question)
    selected_department = route_to_department.plan(
        title=suggested_title, departments=ALL_DEPARTMENTS
    )
    suggested_answers = suggest_department_answers.plan(
        question=question, department=selected_department
    )

    sequence_task = Sequence(suggested_answers, reduce_strategy="CoT")

    res = sequence_task()

    return {
        "question_title": res["question_title"],
        "question": question,
        "department": res["department"],
        "answers": res["answers"],
    }


print(
    handle_customer_question(
        "Hey, I'm not using my account anymore. "
        "I've already talked to customer support and am not interested in it anymore. "
        "Who should I talk to about this?"
    )
)

# {
#     'question_title': 'Account Deactivation Assistance',
#     'question': "Hey, I'm not using my account anymore. I've already talked to customer support and am not interested in it anymore. "
#                 "Who should I talk to about this?",
#     'department': 'support', 
#     'answers': [
#         'You can contact our support team at support@example.com for account deactivation assistance.',
#         'Alternatively, you can also reach out to our live chat support for immediate assistance regarding account deactivation.'
#     ]
# }
```
