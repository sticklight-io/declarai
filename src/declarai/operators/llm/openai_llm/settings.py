"""
Environment level configurations for working with openai provider.
"""
import os

from declarai.core.core_settings import DECLARAI_PREFIX

OPENAI_API_KEY: str = os.getenv(f"{DECLARAI_PREFIX}_OPENAI_API_KEY", "")
OPENAI_MODEL: str = os.getenv(f"{DECLARAI_PREFIX}_OPENAI_MODEL", "gpt-3.5-turbo")
