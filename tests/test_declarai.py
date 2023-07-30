from unittest.mock import MagicMock, patch

from declarai import Declarai


@patch("declarai.task_decorator.LLMTask")
@patch("declarai.declarai.resolve_llm_from_config")
def test_task(mock_llm, mock_llm_task):
    mock_llm_task.return_value = MagicMock()
    mock_llm_task.return_value.return_value = "prediction"
    declarai = Declarai(provider="test", model="test")

    @declarai.task
    def test_task(a: str, b: int) -> str:
        """
        This is a test task
        :param a: this is a string
        :param b: this is an integer
        :return: returns an string
        """
        return declarai.magic("return_name", a=a, b=b)

    assert mock_llm_task.called
    assert test_task.__name__ == "test_task"
    assert test_task.parsed_function
    assert test_task.parsed_function.magic.return_name == "return_name"
    assert test_task.llm_translator

    res = test_task(a="a", b=1)
    assert res == mock_llm_task.return_value.return_value
