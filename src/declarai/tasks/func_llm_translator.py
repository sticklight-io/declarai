from declarai.python_parser import ParsedFunction

FORMAT_INSTRUCTIONS = (
    "The output should be a markdown code snippet formatted in the following schema, "
    "including the leading and trailing '```json' and '```':"
)
JSON_SNIPPET_TEMPLATE = "```json\n{{{{\n    {format}\n}}}}\n```"
INPUTS_TEMPLATE = "Inputs:\n{inputs}\n"
INPUT_LINE_TEMPLATE = "{param}: {{{param}}}"
NEW_LINE_INPUT_LINE_TEMPLATE = "\n{param}: {{{param}}}"


class FunctionLLMTranslator:
    def __init__(self, parsed_function: ParsedFunction):
        self.parsed_func = parsed_function

    def make_input_prompt(self) -> str:
        doc_params = self.parsed_func.doc_params
        input_prompt = ""
        for k, v in self.parsed_func.func_args.items():
            if param_doc := doc_params.get(k):
                input_prompt += f"{k}: {v},  # {param_doc}\n"
            else:
                input_prompt += f"{k}: {v},\n"
        return input_prompt

    def make_input_placeholder(self) -> str:
        """
        Creates a placeholder for the input of the function.
        The input format is based on the function input schema.

        for example a function signature of:
            def foo(a: int, b: str, c: float = 1.0):

        will result in the following placeholder:
            Inputs:
            a: {a}
            b: {b}
            c: {c}
        """
        inputs = ""

        for i, param in enumerate(self.parsed_func.func_args.keys()):
            if i == 0:
                inputs += INPUT_LINE_TEMPLATE.format(param=param)
                continue
            inputs += NEW_LINE_INPUT_LINE_TEMPLATE.format(param=param)

        return INPUTS_TEMPLATE.format(inputs=inputs)

    def make_output_prompt(self) -> str:
        return_type = self.parsed_func.return_type
        return_doc = self.parsed_func.return_doc
        return_name = self.parsed_func.return_name or "result"

        if return_doc:
            output_schema = f"{return_name}: {return_type}  # {return_doc}"
            instructions = (
                FORMAT_INSTRUCTIONS
                + "\n"
                + JSON_SNIPPET_TEMPLATE.format(format=output_schema)
            )
            return instructions

        return ""
