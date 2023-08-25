"""Main interface for declarai.

Decorates the package functionalities and serve as the main interface for the user.
"""
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
        @declarai.task
        def add(a: int, b: int) -> int:
            return magic(a, b)
        ```
    """
    pass


class DeclaraiContext:
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

    def __init__(self, provider: str, model: str = None, **kwargs):
        self.llm = resolve_llm(provider, model, **kwargs)
        self.task = TaskDecorator(self.llm).task

        class Experimental:
            chat = ChatDecorator(self.llm).chat

        self.experimental = Experimental


class Declarai:
    """
    A root interface to declarai.
    This class is a factory to build declarai context.

    There are overloads for the constructor that allow for a more declarative way of building the declarai context
    based on the provider and model.

    Args:
        **kwargs: A set of keyword arguments that are passed to the LLMSettings class.

    """

    magic = magic

    @overload
    def __new__(
        cls,
        provider: ProviderOpenai,
        model: ModelsOpenai,
        version: Optional[str] = None,
        openai_token: Optional[str] = None,
    ) -> DeclaraiContext:
        ...

    def __new__(cls, *args, **kwargs) -> DeclaraiContext:
        """
        Creates a declarai context.

        Args:
            *args:
            **kwargs:
        """
        return DeclaraiContext(*args, **kwargs)

    # *-------------------------------------------------------------------------- *
    # * Custom overloads to enforce the relationship between PROVIDER and MODELS  *
    # * Additionally supported providers should be exposed via the Declarai class *
    # * here:                                                                     *
    # *-------------------------------------------------------------------------- *

    @staticmethod
    def openai(
        model: ModelsOpenai,
        version: str = None,
        openai_token: str = None,
        headers: dict = None,
        timeout: int = None,
        stream: bool = None,
        request_timeout: int = None,
    ) -> DeclaraiContext:
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
            DeclaraiContext: Initialized Declarai context.
        """
        return DeclaraiContext(
            provider=ProviderOpenai,
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
    ) -> DeclaraiContext:
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
        return DeclaraiContext(
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

    @staticmethod
    def register_llm(provider: str, llm_cls: Type[LLM], model: str = None):
        """
        Registers an LLM.
        Args:
            provider: Name of the LLM provider.
            model: Specific model name (optional).
            llm_cls: The LLM class to register.
        """
        llm_registry.register(provider=provider, llm_cls=llm_cls, model=model)

    @staticmethod
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
