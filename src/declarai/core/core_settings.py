"""
This module contains the core settings for the declarai project.
In order to create proper separation from existing code on the client's environment,
we require all environment variables used by `declarai` be prefixed with `DECLARAI_`.
This way we do not interfere with any existing environment variables.
"""

DECLARAI_PREFIX = "DECLARAI"
