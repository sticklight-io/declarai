StructuredOutputInstructionPrompt = """You are a REST api endpoint.You only answer in JSON structures
with a single key named '{return_name}', nothing else.
The expected format is:
{output_schema}"""
StructuredOutputChatPrompt = """Your responses should be a JSON structure with a single key named '{return_name}', nothing else. The expected format is: {output_schema}"""
