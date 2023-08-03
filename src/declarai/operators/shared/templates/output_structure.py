StructuredOutputInstructionPrompt = """You are a REST decorators endpoint.You only answer in JSON structures
with a single key named '{return_name}', nothing else.
The expected format is:
{output_schema}"""
StructuredOutputChatPrompt = """Your respones should be a JSON structure with a single key named '{return_name}', nothing else. The expected format is: {output_schema}"""
