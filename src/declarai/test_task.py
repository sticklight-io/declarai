from unittest.mock import MagicMock, patch

from .task import init_declarai, magic


@patch("src.declarai.task.LLMTask")
@patch("src.declarai.task.resolve_llm_from_config")
def test_task(mock_llm, mock_llm_task):
    mock_llm_task.return_value = MagicMock()
    mock_llm_task.return_value.return_value = "prediction"
    declarai = init_declarai(provider="test", model="test")

    @declarai
    def test_task(a: str, b: int) -> str:
        """
        This is a test task
        :param a: this is a string
        :param b: this is an integer
        :return: returns an string
        """
        return magic("return_name", a, b)

    assert mock_llm_task.called
    assert test_task.__name__ == "test_task"
    assert test_task.parsed_function
    assert test_task.parsed_function.magic == "return_name"
    assert test_task.llm_translator

    res = test_task(a="a", b=1)
    assert res == mock_llm_task.return_value.return_value
