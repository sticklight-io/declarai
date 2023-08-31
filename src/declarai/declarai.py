"""Main interface for declarai.

Decorates the package functionalities and serve as the main interface for the user.
"""
import warnings
from typing import Any, Dict, Optional, Type, overload

from declarai.chat import ChatDecorator
from declarai.operators import (
    LLM,
    BaseOperator,
    ModelsOpenai,
    ProviderAzureOpenai,
    ProviderOpenai,
    llm_registry,
    operator_registry,
    resolve_llm,
)
from declarai.task import TaskDecorator

SUPPORT_018_BACK_COMPAT = True


def magic(
    return_name: Optional[str] = None,
    *,
    task_desc: Optional[str] = None,
    input_desc: Optional[Dict[str, str]] = None,
    output_desc: Optional[str] = None,
    **kwargs
) -> Any:
    """
    This is an empty method used as a potential replacement for using the docstring for passing
    parameters to the LLM builder. It can also serve as a fake use of arguments in the defined
    functions as to simplify handling of lint rules for llms functions.

    Example:
        ```py
        @openai.task
        def add(a: int, b: int) -> int:
            return magic(a, b)
        ```
    """
    pass


class Declarai:
    """
    Context manager for the Declarai root interface.
    This class is responsible for setting up tasks and initializing experimental features
    provided by Declarai.

    Args:
        provider (str): The provider name.
        model (str): The model name.
        **kwargs: Additional keyword arguments passed to the LLM resolver.

    Attributes:
        llm (LLM): Resolved LLM.
        task (Callable): A decorator for task creation.
        experimental: A namespace for experimental features.
        experimental.chat (Callable): A decorator for chat operators.
    """

    if SUPPORT_018_BACK_COMPAT:

        @staticmethod
        def openai(
            model: ModelsOpenai,
            version: str = None,
            openai_token: str = None,
            headers: dict = None,
            timeout: int = None,
            stream: bool = None,
            request_timeout: int = None,
        ):
            warnings.warn(
                "Declarai.openai is deprecated. Will be removed in 0.2.*. Please use `import declarai; declarai.openai`",
                DeprecationWarning,
            )
            openai(
                model=model,
                version=version,
                openai_token=openai_token,
                headers=headers,
                timeout=timeout,
                stream=stream,
                request_timeout=request_timeout,
            )

        @staticmethod
        def azure_openai(
            deployment_name: str,
            azure_openai_key: str = None,
            azure_openai_api_base: str = None,
            api_version: str = None,
            headers: dict = None,
            timeout: int = None,
            stream: bool = None,
            request_timeout: int = None,
        ):
            warnings.warn(
                "Declarai.azure_openai is deprecated. Will be removed in 0.2.*. Please use `import declarai; declarai.azure_openai`",
                DeprecationWarning,
            )
            azure_openai(
                deployment_name=deployment_name,
                azure_openai_key=azure_openai_key,
                azure_openai_api_base=azure_openai_api_base,
                api_version=api_version,
                headers=headers,
                timeout=timeout,
                stream=stream,
                request_timeout=request_timeout,
            )

    @overload
    def __init__(
        self,
        provider: ProviderOpenai,
        model: ModelsOpenai,
        version: Optional[str] = None,
        openai_token: Optional[str] = None,
        stream: Optional[bool] = None,
    ):
        ...

    @overload
    def __init__(
        self,
        provider: ProviderAzureOpenai,
        model: str,
        stream: Optional[bool] = None,
        **kwargs
    ):
        ...

    def __init__(self, provider: str, model: str, **kwargs):
        self.llm = resolve_llm(provider, model, **kwargs)
        self.task = TaskDecorator(self.llm).task

        class Experimental:
            chat = ChatDecorator(self.llm).chat

        self.experimental = Experimental


def openai(
    model: ModelsOpenai,
    version: str = None,
    openai_token: str = None,
    headers: dict = None,
    timeout: int = None,
    stream: bool = None,
    request_timeout: int = None,
) -> Declarai:
    """
    Sets up a Declarai context for the OpenAI provider.

    Args:
        model (ModelsOpenai): The model to be used.
        version (str, optional): Model version.
        openai_token (str, optional): OpenAI authentication token.
        headers (dict, optional): Additional headers for the request.
        timeout (int, optional): Timeout for the request.
        stream (bool, optional): Whether to stream the response.
        request_timeout (int, optional): Request timeout duration.

    Returns:
        Declarai: Initialized Declarai context.
    """
    return Declarai(
        provider=ProviderOpenai,
        model=model,
        version=version,
        openai_token=openai_token,
        headers=headers,
        timeout=timeout,
        stream=stream,
        request_timeout=request_timeout,
    )


def azure_openai(
    deployment_name: str,
    azure_openai_key: str = None,
    azure_openai_api_base: str = None,
    api_version: str = None,
    headers: dict = None,
    timeout: int = None,
    stream: bool = None,
    request_timeout: int = None,
) -> Declarai:
    """
    Sets up a Declarai context for the Azure OpenAI provider.

    Args:
        deployment_name (str): Name of the deployment.
        azure_openai_key (str, optional): Azure OpenAI key.
        azure_openai_api_base (str, optional): Base API URL for Azure OpenAI.
        api_version (str, optional): API version.
        headers (dict, optional): Additional headers for the request.
        timeout (int, optional): Timeout for the request.
        stream (bool, optional): Whether to stream the response.
        request_timeout (int, optional): Request timeout duration.

    Returns:
        DeclaraiContext: Initialized Declarai context.
    """
    return Declarai(
        provider=ProviderAzureOpenai,
        model=deployment_name,
        azure_openai_key=azure_openai_key,
        azure_openai_api_base=azure_openai_api_base,
        api_version=api_version,
        headers=headers,
        timeout=timeout,
        stream=stream,
        request_timeout=request_timeout,
    )


def register_llm(provider: str, llm_cls: Type[LLM], model: str = None):
    """
    Registers an LLM.
    Args:
        provider: Name of the LLM provider.
        model: Specific model name (optional).
        llm_cls: The LLM class to register.
    """
    llm_registry.register(provider=provider, llm_cls=llm_cls, model=model)


def register_operator(
    provider: str,
    operator_type: str,
    operator_cls: Type[BaseOperator],
    model: str = None,
):
    """
    Registers an operator.
    Args:
        provider: Name of the LLM provider.
        operator_type: The type of operator (e.g., "chat", "task").
        operator_cls: The operator class to register.
        model: Specific model name
    """
    operator_registry.register(
        provider=provider,
        operator_type=operator_type,
        model=model,
        operator_cls=operator_cls,
    )


def _patch_back_compat():
    Declarai.openai = openai
    Declarai.azure_openai = azure_openai


if SUPPORT_018_BACK_COMPAT:
    _patch_back_compat()
