"""
The prompt templates for the format of the output.
"""
StructuredOutputInstructionPrompt = """You are a REST api endpoint.You only answer in JSON structures
with a single key named '{return_name}', nothing else.
The expected format is:
{output_schema}"""
"."  # for documentation purposes


StructuredOutputChatPrompt = """Your responses should be a JSON structure with a single key named '{return_name}', nothing else. The expected format is: {output_schema}"""  # noqa

"."  # for documentation purposes
