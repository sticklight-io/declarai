# from typing import Dict
# from unittest.mock import MagicMock
#
# from declarai.orchestrator.future_llm_task import FutureTask
# from declarai.operators.base.types import LLMTask
#
# TEST_TASK_TEMPLATE = "{input} | {output}"
# TEMPLATE_KWARGS = {
#     "input": "input-value: {input_val}",
#     "output": "output-value: {output_val}",
# }
# TASK_KWARGS = {
#     "input_val": "input-value",
#     "output_val": "output-value",
# }
#
#
# def test_llm_task():
#     test_llm = MagicMock()
#     test_llm.predict.return_value = MagicMock()
#     test_llm.predict.return_value.response = '{"declarai_result": "output-value"}'
#
#     llm_task = LLMTask(
#         template=TEST_TASK_TEMPLATE,
#         template_kwargs=TEMPLATE_KWARGS,
#         llm=test_llm,
#         prompt_kwargs={"return_type": str},
#     )
#
#     compiled_task_template = "input-value: {input_val} | output-value: {output_val}"
#     compiled_task_with_values = "input-value: input-value | output-value: output-value"
#
#     assert llm_task.compile() == compiled_task_template
#     assert llm_task.compile(**TASK_KWARGS) == compiled_task_with_values
#
#     llm_res = llm_task(**TASK_KWARGS)
#     assert llm_res == "output-value"
#     assert test_llm.predict.called
#
#
# def test_llm_task_result_name_override():
#     test_llm = MagicMock()
#     test_llm.predict.return_value = MagicMock()
#     test_llm.predict.return_value.response = '{"result": "output-value"}'
#
#     llm_task = LLMTask(
#         template=TEST_TASK_TEMPLATE,
#         template_kwargs=TEMPLATE_KWARGS,
#         llm=test_llm,
#         prompt_kwargs={
#             "return_name": "result",
#             "return_type": str,
#         },
#     )
#     compiled_task_template = "input-value: {input_val} | output-value: {output_val}"
#     compiled_task_with_values = "input-value: input-value | output-value: output-value"
#     assert llm_task.compile() == compiled_task_template
#     assert llm_task.compile(**TASK_KWARGS) == compiled_task_with_values
#
#     llm_res = llm_task(**TASK_KWARGS)
#     assert llm_res == "output-value"
#     assert test_llm.predict.called
#
#
# def test_llm_task_unstructured_result():
#     test_llm = MagicMock()
#     test_llm.predict.return_value = MagicMock()
#     test_llm.predict.return_value.response = "output-value"
#
#     llm_task = LLMTask(
#         template=TEST_TASK_TEMPLATE,
#         template_kwargs=TEMPLATE_KWARGS,
#         llm=test_llm,
#         prompt_kwargs={"structured": False},
#     )
#     llm_res = llm_task(**TASK_KWARGS)
#     assert llm_res == "output-value"
#     assert test_llm.predict.called
#
#
# def test_llm_task_multiple_results():
#     test_llm = MagicMock()
#     test_llm.predict.return_value = MagicMock()
#     test_llm.predict.return_value.response = (
#         '{"result1": "output-value1"}\n\n\n{"result2": "output-value2"}'
#     )
#
#     llm_task = LLMTask(
#         template=TEST_TASK_TEMPLATE,
#         template_kwargs=TEMPLATE_KWARGS,
#         llm=test_llm,
#         prompt_kwargs={"multi_results": True},
#     )
#     llm_res = llm_task(**TASK_KWARGS)
#     assert llm_res == {"result1": "output-value1", "result2": "output-value2"}
#     assert test_llm.predict.called
#
#
# def test_future_llm_task():
#     test_llm = MagicMock()
#     test_llm.predict.return_value = MagicMock()
#     test_llm.predict.return_value.response = '{"declarai_result": "output-value"}'
#
#     llm_task = LLMTask(
#         template=TEST_TASK_TEMPLATE,
#         template_kwargs=TEMPLATE_KWARGS,
#         llm=test_llm,
#         prompt_kwargs={"return_type": str},
#     )
#     compiled_task_with_values = "input-value: input-value | output-value: output-value"
#     future_task = llm_task.plan(**TASK_KWARGS)
#     assert isinstance(future_task, FutureTask)
#     assert future_task.populated_prompt == compiled_task_with_values
#     assert future_task() == "output-value"
