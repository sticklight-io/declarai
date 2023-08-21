from unittest.mock import MagicMock, patch

from declarai.declarai import magic
from declarai.task import TaskDecorator


@patch("declarai.task.PythonParser")
@patch("declarai.task.resolve_operator")
def test_task_decorator_no_args(mocked_resolve_operator, mocked_python_parser):
    llm_settings = MagicMock()
    operator_class_mock = MagicMock()
    operator_instance_mock = MagicMock()
    llm = MagicMock()
    middleware = MagicMock()

    # Setting up mocks
    mocked_python_parser.return_value = MagicMock()
    operator_instance_mock.parsed = mocked_python_parser.return_value
    operator_class_mock.return_value = operator_instance_mock
    mocked_resolve_operator.return_value = (operator_class_mock, llm)

    middlewares = [middleware]

    task_decorator = TaskDecorator(
        llm_settings=llm_settings, middlewares=middlewares
    )
    decorator = task_decorator.task

    @decorator(
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

    assert task_decorator.llm_settings == llm_settings
    assert test_task.middlewares == middlewares
    assert test_task.__name__ == "test_task"
    assert test_task.operator.parsed == mocked_python_parser.return_value
    assert test_task.operator == operator_instance_mock
    passed_llm = operator_class_mock.call_args.kwargs['llm']
    assert passed_llm == llm


    @decorator(
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

    passed_llm_params = operator_class_mock.call_args.kwargs['llm_params']
    assert passed_llm_params == {"temperature": 0.5}
    assert test_task.__name__ == "test_task"
    assert test_task.middlewares == middlewares

    @decorator(
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
    passed_llm_params = operator_class_mock.call_args.kwargs['llm_params']
    assert passed_llm_params == {"temperature": 0.5}
    operator_instance_mock.predict.assert_called_with(llm_params={"temperature": 0.7})
