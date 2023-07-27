from pprint import pprint
from typing import Any, Dict, List

from declarai import Sequence, init_declarai, magic

declarai = init_declarai(provider="openai", model="gpt-3.5-turbo-0301")


@declarai
def suggest_title(question: str) -> str:
    """
    Given a question from our customer support, suggest a title for it
    :param question: the provided question
    :return: The title suggested for the question
    """
    return magic("question_title", question)


@declarai
def route_to_department(title: str, departments: List[str]) -> str:
    """
    Given a question title, route it to the relevant department
    :param title: A title generated for the question
    :param departments: The departments to route the question to
    :return: The department that the question should be routed to
    """
    return magic("department", title, departments)


@declarai
def suggest_department_answers(title: str, department: str) -> List[str]:
    """
    Given a question and a department, suggest 2 answers from the department's knowledge base
    :param title: The question title to suggest answers for
    :param department: The department to suggest answers from
    :return: The suggested answers
    """
    return magic("answers", title, department)


available_departments = ["sales", "support", "billing"]


def handle_customer_question(question: str) -> Dict[str, Any]:
    suggested_title = suggest_title.plan(question=question)
    selected_department = route_to_department.plan(
        title=suggested_title, departments=available_departments
    )
    suggested_answers = suggest_department_answers.plan(
        title=suggested_title, department=selected_department
    )

    reduced_task = Sequence(suggested_answers, reduce_strategy="CoT")
    res = reduced_task()

    return {
        "question_title": res["question_title"],
        "question": question,
        "department": res["department"],
        "answers": res["answers"],
    }


pprint(
    handle_customer_question(
        "Hey, I'm not using my account anymore. "
        "I've already talked to customer support and am not interested in it anymore. "
        "Who should I talk to about this?"
    )
)
