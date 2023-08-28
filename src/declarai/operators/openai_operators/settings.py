"""
Environment level configurations for working with openai and Azure openai providers.
"""
import os
from declarai.core.core_settings import DECLARAI_PREFIX

OPENAI_API_KEY: str = os.getenv(
    f"{DECLARAI_PREFIX}_OPENAI_API_KEY", os.getenv("OPENAI_API_KEY", "")
)  # pylint: disable=E1101
"API key for openai provider."

OPENAI_MODEL: str = os.getenv(
    f"{DECLARAI_PREFIX}_OPENAI_MODEL", "gpt-3.5-turbo"
)  # pylint: disable=E1101
"Model name for openai provider."

# Azure specific configurations
AZURE_OPENAI_KEY: str = os.getenv(
    f"{DECLARAI_PREFIX}_AZURE_OPENAI_KEY", os.getenv("AZURE_OPENAI_KEY", "")
)  # pylint: disable=E1101
"API key for Azure openai provider."

AZURE_OPENAI_API_BASE: str = os.getenv(
    f"{DECLARAI_PREFIX}_AZURE_OPENAI_API_BASE",
    os.getenv("AZURE_OPENAI_API_BASE", ""),
)  # pylint: disable=E1101
"Endpoint for Azure openai provider."

AZURE_API_VERSION: str = os.getenv(
    f"{DECLARAI_PREFIX}_AZURE_API_VERSION",
    os.getenv("AZURE_API_VERSION", "2023-05-15"),
)  # pylint: disable=E1101
"API version for Azure openai provider."


DEPLOYMENT_NAME: str = os.getenv(
    f"{DECLARAI_PREFIX}_AZURE_OPENAI_DEPLOYMENT_NAME",
    os.getenv("DEPLOYMENT_NAME", ""),
)  # pylint: disable=E1101
"Deployment name for the model in Azure openai provider."
