from unittest.mock import MagicMock, patch

from declarai import Declarai


@patch("declarai.api.chat_decorator.resolve_operator")
@patch("declarai.declarai.LLMTaskDecorator")
@patch("declarai.declarai.LLMSettings")
def test_declarai(mocked_llm_settings, mocked_task_decorator, _):
    kwargs = {}
    mocked_llm_settings.return_value = MagicMock()
    mocked_task_decorator.return_value = MagicMock()

    declarai = Declarai(**kwargs)

    assert declarai.llm_config == mocked_llm_settings.return_value
    assert declarai.task == mocked_task_decorator.return_value

    # Test experimental apis
    assert declarai.experimental
