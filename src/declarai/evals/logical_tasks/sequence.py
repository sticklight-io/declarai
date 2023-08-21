# from typing import List
#
# from declarai import Declarai
# from declarai.orchestrator.sequence import Sequence
#
#
# def suggest_title(question: str) -> str:
#     """
#     Given a question from our customer support, suggest a title for it
#     :param question: the provided question
#     :return: The title suggested for the question
#     """
#     return Declarai.magic("question_title", question)
#
#
# def route_to_department(title: str, departments: List[str]) -> str:
#     """
#     Given a question title, route it to the relevant department
#     :param title: A title generated for the question
#     :param departments: The departments to route the question to
#     :return: The department that the question should be routed to
#     """
#     return Declarai.magic("department", title, departments)
#
#
# def suggest_department_answers(title: str, department: str) -> List[str]:
#     """
#     Given a question and a department, suggest 2 answers from the department's knowledge base
#     :param title: The question title to suggest answers for
#     :param department: The department to suggest answers from
#     :return: The suggested answers
#     """
#     return Declarai.magic("answers", title, department)
#
#
# available_departments = ["sales", "support", "billing"]
#
#
# def chain_of_thought(declarai: Declarai, question: str):
#     suggested_title_task = declarai.task(suggest_title)
#     selected_department_task = declarai.task(route_to_department)
#     department_answers_task = declarai.task(suggest_department_answers)
#
#     suggested_title = suggested_title_task.plan(question=question)
#     selected_department = selected_department_task.plan(
#         title=suggested_title, departments=available_departments
#     )
#     suggested_answers = department_answers_task.plan(
#         title=suggested_title, department=selected_department
#     )
#
#     return Sequence(suggested_answers, reduce_strategy="CoT")
#
#
# chain_of_thought_kwargs = {
#     "question": "Hey, I'm not using my account anymore. "
#     "I've already talked to customer support and am not interested in it anymore. "
#     "Who should I talk to about this?"
# }
