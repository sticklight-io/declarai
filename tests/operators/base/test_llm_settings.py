from declarai.operators import LLMSettings


def test_llm_settings():
    llm_settings = LLMSettings(
        provider="test-provider",
        model="test-model",
        version="test-version",
    )

    assert llm_settings.provider == "test-provider"
    assert llm_settings.model == "test-model-test-version"
    assert llm_settings.version == "test-version"
