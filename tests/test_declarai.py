from unittest.mock import patch, MagicMock

from declarai import Declarai


@patch("declarai.declarai.LLMTaskDecorator")
@patch("declarai.declarai.LLMSettings")
def test_declarai(mocked_llm_settings, mocked_task_decorator):
    kwargs = {}
    mocked_llm_settings.return_value = MagicMock()
    mocked_task_decorator.return_value = MagicMock()

    declarai = Declarai(**kwargs)

    assert declarai.llm_config == mocked_llm_settings.return_value
    assert declarai.task == mocked_task_decorator.return_value

    # Test experimental apis
    assert declarai.Experimental
