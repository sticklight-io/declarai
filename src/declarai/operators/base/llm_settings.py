from typing import Optional


class LLMSettings:
    def __init__(
        self,
        provider: str,
        model: str,
        version: Optional[str] = None,
        **_,
    ):
        self.provider = provider
        self._model = model
        self.version = version

    @property
    def model(self, delimiter: Optional[str] = "-") -> str:
        """
        Some model providers allow defining a base model as well as a sub-model.
        Often the base model is an alias to latest model served on that model.
        for example, when sending gpt-3.5-turbo to OpenAI, the actual model will be one of the
        publicly available snapshots or an internally exposed version as described on their website:
        as of 27/07/2023 - https://platform.openai.com/docs/models/continuous-model-upgrades
        | With the release of gpt-3.5-turbo, some of our models are now being continually updated.
        | We also offer static model versions that developers can continue using for at least
        | three months after an updated model has been introduced.

        Another use-case for sub models is using your own fine-tuned models.
        As described in the documentation:
        https://platform.openai.com/docs/guides/fine-tuning/customize-your-model-name

        You will likely build your fine-tuned model names by concatenating the base model name
        with the fine-tuned model name, separated by a hyphen.
        For example
        gpt-3.5-turbo-declarai-text-classification-2023-03
        or
        gpt-3.5-turbo:declarai:text-classification-2023-03

        In any case you can always pass the full model name in the model parameter and leave the
        sub_model parameter empty if you prefer.
        """
        if self.version:
            return f"{self._model}{delimiter}{self.version}"
        return self._model
