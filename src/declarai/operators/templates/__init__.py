"""
This module contains the shared templates for the operators.
"""
from .chain_of_thought import ChainOfThoughtsTemplate
from .instruct_function import InstructFunctionTemplate
from .output_prompt import compile_output_prompt, compile_output_schema_template
from .output_structure import (
    StructuredOutputChatPrompt,
    StructuredOutputInstructionPrompt,
)
