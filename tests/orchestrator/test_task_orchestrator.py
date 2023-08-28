from unittest.mock import MagicMock

from declarai.python_parser.parser import PythonParser
from declarai.task import Task


def test_task():
    operator = MagicMock()
    instantiated_operator = MagicMock()
    operator.return_value = instantiated_operator

    instantiated_operator.compile.return_value = "compiled_result"
    llm_response = MagicMock()
    llm_response.response = "predicted_result"
    instantiated_operator.predict.return_value = llm_response

    def test_task() -> str:
        pass

    instantiated_operator.parse_output.return_value = PythonParser(test_task).parse(
        llm_response.response
    )

    task = Task(instantiated_operator)
    assert task.compile() == "compiled_result"

    # TODO: Implement test when plan is implemented
    # task_orchestrator.plan()

    res = task()
    assert res == "predicted_result"

    res = task(llm_params={"temperature": 0.5})
    instantiated_operator.predict.assert_called_with(llm_params={"temperature": 0.5})
