"""
Registry for LLMs and Operators.
"""
from collections import defaultdict
from typing import Type, Optional

from declarai.operators.llm import LLM
from declarai.operators.operator import BaseOperator


class LLMRegistry:
    """
    Registry for LLMs.
    The registry will have a nested structure: {provider: {model: llm_cls}}
    But it will also support a direct provider-to-llm_cls mapping for generic LLMs.
    But it will also support a direct provider-to-llm_cls mapping for generic LLMs.
    """

    def __init__(self):
        self._registry = defaultdict(dict)

    def register(
        self, provider: str, llm_cls: Type[LLM], model: Optional[str] = "default"
    ):
        """
        Registers an LLM.
        Args:
            provider: the name of the LLM provider.
            llm_cls: the LLM class to register.
            model: the specific model name.

        Returns:
            None

        """
        self._registry[provider][model] = llm_cls

    def resolve(self, provider: str, model: Optional[str] = None, **kwargs) -> LLM:
        """
        Resolves an LLM. If the model is not specified, the default model of the given provider will be used.
        Args:
            provider: the name of the LLM provider.
            model: the specific model name.
            **kwargs: Additional keyword arguments to pass to the LLM initialization.

        Returns:
            An LLM instance.
        """
        if not model:
            model = "default"
        provider_registry = self._registry.get(provider, {})

        llm_cls = provider_registry.get(model)
        if not llm_cls:
            # If the specific model isn't found, fall back to the default.
            llm_cls = provider_registry.get("default")

        if not llm_cls:
            raise NotImplementedError(
                f"LLMProvider : {provider} or model: {model} not implemented"
            )
        try:
            return llm_cls(model=model, **kwargs)
        except TypeError:
            return llm_cls(**kwargs)


llm_registry = LLMRegistry()
"""The global LLM registry."""


# Example registrations
# For a provider that supports all models with the same LLM:
# llm_registry.register(ProviderOpenai, llm_cls=GenericOpenAILLM)

# For a specific model under a provider:
# llm_registry.register(ProviderAzureOpenai, model="azure-specific-model", llm_cls=AzureSpecificLLM)


# Operator Registry
class OperatorRegistry:
    """
    Registry for Operators.
    The registry will have a nested structure: {provider: {operator_type: {model: operator_cls}}}
    It will support a direct provider-to-operator_cls mapping for generic Operators.
    """

    def __init__(self):
        self._registry = defaultdict(lambda: defaultdict(dict))

    def register(
        self,
        provider: str,
        operator_type: str,
        operator_cls: Type[BaseOperator],
        model: str = "default",
    ):
        """
        Registers an operator.

        Args:
            provider: the name of the operator provider.
            operator_type: the type of the operator.
            operator_cls: the operator class to register.
            model: the specific model name that the operator is registered to.

        Returns:
            None

        """
        self._registry[provider][operator_type][model] = operator_cls

    def resolve(self, llm_instance: LLM, operator_type: str) -> Type[BaseOperator]:
        """
        Resolves an operator.

        Args:
            llm_instance: An LLM instance.
            operator_type: A string representing the type of the operator.

        Returns:
            An operator class.

        """
        default_model = "default"
        provider = llm_instance.provider
        operator_registry = self._registry.get(provider, {})

        specific_operator_registry = operator_registry.get(operator_type, {})
        operator_cls = specific_operator_registry.get(llm_instance.model)

        if not operator_cls:
            # If the specific model isn't found, fall back to the default.
            operator_cls = specific_operator_registry.get(default_model)

        if not operator_cls:
            raise NotImplementedError(
                f"Operator type : {operator_type} for provider: {provider} or model: {llm_instance.model} not implemented"
            )

        return operator_cls


operator_registry = OperatorRegistry()
"""The global Operator registry."""


def register_llm(provider: str, model: Optional[str] = "default"):
    """
    A decorator that registers an LLM class to the LLM registry.

    Args:
        provider: the name of the LLM provider.
        model: the specific model name.

    Returns:
        A decorator that registers the decorated LLM class to the LLM registry.
    """

    def decorator(cls):
        llm_registry.register(provider, cls, model)
        return cls

    return decorator


def register_operator(
    provider: str, operator_type: str, model: Optional[str] = "default"
):
    """
    A decorator that registers an operator class to the operator registry.

    Args:
        provider: the name of the operator provider.
        operator_type: the string representing the type of the operator.
        model: the specific model name.

    Returns:
        A decorator that registers the decorated operator class to the operator registry.

    """

    def decorator(cls):
        operator_registry.register(provider, operator_type, cls, model)
        return cls

    return decorator
