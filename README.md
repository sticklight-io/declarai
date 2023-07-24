# Introducing declareai
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
from declarai import magic, task

@task
def extract_email_info(text: str, contact_fields: List[str]) -> Dict[str, str]:
    """
    Extract the provided contact fields from the given text
    :param text: The text to extract contact information from
    :param contact_fields: The contact fields to extract
    :return: A mapping of the contact fields to their values
    """
    return magic(text, contact_fields)


res = extract_email_info(
    text="I am John Doe and my phone number is 123-456-7890." 
         "My email address is johndoe@coolmail.co.il",
    contact_fields=["phone", "name", "email"],
)
print(res)
# {'phone': '123-456-7890', 'name': 'John Doe', 'email': 'johndoe@coolmail.co.il'}
```
That's it! You've written your first AI code!

declarai aims to promote clean and readable code by enforcing the use of doc-strings and typing.
The resulting code is readable and easily maintainable.

For more complex use cases you can use a reducer, to build and compile multiple prompts into one!
```python
from typing import Any, Dict, List
from declarai import Reducer, magic, task


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


departments = ["sales", "support", "billing"]

def handle_customer_question(question: str) -> Dict[str, Any]:
    plan = Reducer()
    plan.add("question_title", suggest_title, question=question)
    plan.add("department", route_to_department, title=plan["question_title"], departments=departments)
    plan.add("answers", suggest_department_answers, question=question, department=plan["department"])

    res = plan.execute()

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
#     'question_title': 'I want to cancel my account',
#     'question': "Hey, I'm not using my account anymore. I've already talked to customer support and am not interested in it anymore. Who should I talk to about this?",
#     'department': 'billing',
#     'answers': [
#         'You can cancel your account by going to the billing page and clicking the cancel button',
#         'You can contact support to cancel your account via the following email: support@coolmailco',
#     ]
```

## Debugging
If you want to see what's going on under the hood, you can compile your code before execution:
```python
print(plan.compile())
# The following task should be done in 3 steps:
# Use the output of the previous step as the input of the next step.
# Step 1: 
# Given a question from our customer support, suggest a title for it
# Inputs:
# question: Hey, I'm not using my account anymore. I've already talked to customer support and am not interested in it anymore. Who should I talk to about this?
# The output should be a markdown code snippet formatted in the following schema, including the leading and trailing '```json' and '```':
# ```json
# {
#     question_title: <class 'str'>  #  The title suggested for the question
# }
# ```
# Step 2: 
# Given a question title, route it to the relevant department
# Inputs:
# title: From previous step
# departments: ['sales', 'support', 'billing']
# The output should be a markdown code snippet formatted in the following schema, including the leading and trailing '```json' and '```':
# ```json
# {
#     department: <class 'str'>  #  The department that the question should be routed to
# }
# ```
# Step 3: 
# Given a question and a department, suggest 2 answers from the department's knowledge base
# Inputs:
# question: Hey, I'm not using my account anymore. I've already talked to customer support and am not interested in it anymore. Who should I talk to about this?
# department: From previous step
# The output should be a markdown code snippet formatted in the following schema, including the leading and trailing '```json' and '```':
# ```json
# {
#     answers: typing.List[str]  #  The suggested answers
# }
# ```
# Let's think step by step
```

This output is generated using the `chain of thought` strategy and we will later support additional types of reducer strategies!

