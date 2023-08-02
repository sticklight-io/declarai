# from unittest.mock import MagicMock
#
# from declarai.orchestrator.future_llm_task import FutureLLMTask
#
#
# def test_future_llm_task():
#     exec_func = MagicMock()
#     exec_func.return_value = "output-value"
#     kwargs = {
#         "input": "input-value",
#         "output": "output-value",
#     }
#     compiled_template = "{input} | {output}"
#     populated_prompt = "input-value | output-value"
#
#     future_llm_task = FutureLLMTask(
#         exec_func=exec_func,
#         kwargs=kwargs,
#         compiled_template=compiled_template,
#         populated_prompt=populated_prompt,
#     )
#
#     task_res = future_llm_task()
#     assert task_res == "output-value"
#     exec_func.assert_called_with(populated_prompt)
#
#     assert future_llm_task.populated_prompt == populated_prompt
#
#     assert future_llm_task.compiled_template == compiled_template
#
#     assert future_llm_task.task_kwargs == kwargs
