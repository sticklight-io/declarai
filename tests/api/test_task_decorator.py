from unittest.mock import MagicMock, patch

from declarai.decorators.magic import magic
from declarai.decorators.task_decorator import LLMTaskDecorator


@patch("declarai.orchestrator.task_orchestrator.PythonParser")
@patch("declarai.decorators.task_decorator.resolve_operator")
def test_task_decorator_no_args(mocked_resolve_operator, mocked_python_parser):
    declarai_instance = MagicMock()
    mocked_resolve_operator.return_value = MagicMock()
    mock_operator_instance = (
        mocked_resolve_operator.return_value.return_value
    ) = MagicMock()
    middleware = MagicMock()
    middlewares = [middleware]

    mocked_python_parser.return_value = MagicMock()

    task_decorator = LLMTaskDecorator(
        declarai_instance=declarai_instance, middlewares=middlewares
    )

    @task_decorator(
        middlewares=middlewares,
    )
    def test_task(a: str, b: int) -> str:
        """
        This is a test task
        :param a: this is a string
        :param b: this is an integer
        :return: returns a string
        """
        return magic("return_name", a=a, b=b)

    assert task_decorator.declarai_instance == declarai_instance
    assert task_decorator.operator == mocked_resolve_operator.return_value
    assert test_task.middlewares == middlewares

    assert test_task.__name__ == "test_task"
    assert test_task.parsed == mocked_python_parser.return_value
    assert test_task.operator == mock_operator_instance

    @task_decorator(
        middlewares=middlewares,
        llm_params={"temperature": 0.5}
    )
    def test_task(a: str, b: int) -> str:
        """
        This is a test task
        :param a: this is a string
        :param b: this is an integer
        :return: returns a string
        """

    assert test_task.llm_params == {"temperature": 0.5}
    assert test_task.__name__ == "test_task"
    assert test_task.middlewares == middlewares


    @task_decorator(
        llm_params={"temperature": 0.5}
    )
    def test_task(a: str, b: int) -> str:
        """
        This is a test task
        :param a: this is a string
        :param b: this is an integer
        :return: returns a string
        """

    test_task(llm_params={"temperature": 0.7})
    assert test_task.llm_params == {"temperature": 0.5}
    mocked_resolve_operator().return_value.predict.assert_called_with(llm_params={"temperature": 0.7})
