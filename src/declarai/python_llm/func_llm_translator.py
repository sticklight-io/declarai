import logging

from declarai.python_llm.function_parser import ParsedFunction

FORMAT_INSTRUCTIONS = (
    "The output should be a markdown code snippet formatted in the following schema, "
    "including the leading and trailing '```json' and '```':"
)
JSON_SNIPPET_TEMPLATE = "```json\n{{{{\n    {format}\n}}}}\n```"
INPUTS_TEMPLATE = "Inputs:\n{inputs}\n"
INPUT_LINE_TEMPLATE = "{param}: {{{param}}}"
NEW_LINE_INPUT_LINE_TEMPLATE = "\n{param}: {{{param}}}"


logger = logging.getLogger("generator")


class FunctionLLMTranslator:
    def __init__(self, parsed_function: ParsedFunction):
        self.parsed_func = parsed_function

    def make_input_prompt(self) -> str:

        input_prompt = ""
        for signature_arg, signature_arg_type in self.parsed_func.func_args.items():
            param_doc = doc_params.get(signature_arg)
            if param_doc:
                input_prompt += f"{signature_arg}: {signature_arg_type},  # {param_doc}\n"
            else:
                input_prompt += f"{signature_arg}: {signature_arg_type},\n"
        return input_prompt

    def make_input_placeholder(self) -> str:
        """
        Creates a placeholder for the input of the function.
        The input format is based on the function input schema.

        for example a function signature of:
            def foo(a: int, b: str, c: float = 1.0):

        will result in the following placeholder:
            Inputs:
            a: {a}  # a desc
            b: {b}  # b desc
            c: {c}  # c desc
        """
        inputs = ""
        doc_params = self.parsed_func.params
        magic = self.parsed_func.magic
        param_docs = doc_params.update(magic.input_desc)

        for i, param in enumerate(self.parsed_func.func_args.keys()):
            inputs += INPUT_LINE_TEMPLATE.format(param=param)
            param_doc = param_docs.get(param)
            if param_doc:
                inputs += f"  # {param_doc}"
            if i != 0:
                inputs = f"\n{inputs}"

        return INPUTS_TEMPLATE.format(inputs=inputs)

    def has_any_return_defs(self) -> bool:
        return any(
            [
                self.parsed_func.returns[0],
                self.parsed_func.returns[1],
                self.parsed_func.return_type,
            ]
        )

    def make_output_prompt(self) -> str:
        magic_definition = self.parsed_func.magic
        return_type = self.parsed_func.return_type
        return_name, return_doc = self.parsed_func.returns
        return_name = return_name or magic_definition.return_name or "declarai_result"
        return_doc = return_doc or magic_definition.output_desc

        if not self.has_any_return_defs():
            logger.warning(
                "Couldn't create output schema for function %s."
                "Falling back to unstructured output."
                "Please add at least one of the following: return type, return doc, return name",
                self.parsed_func.name,
            )
            return ""

        output_prompt = make_output_prompt(return_name, return_type, return_doc)
        instructions = (
            FORMAT_INSTRUCTIONS
            + "\n"
            + JSON_SNIPPET_TEMPLATE.format(format=output_prompt)
        )
        return instructions


def make_output_prompt(return_name: str, return_type: str, return_doc: str) -> str:
    if not any([return_name, return_type, return_doc]):
        return ""

    output_schema = f'"{return_name or "declarai_result"}": '

    if return_type:
        output_schema += str(return_type)

    if return_doc:
        if not return_type and not return_name:
            return f"{return_doc}: "
        output_schema += f"  # {return_doc}"

    if not output_schema:
        return ""

    return output_schema
