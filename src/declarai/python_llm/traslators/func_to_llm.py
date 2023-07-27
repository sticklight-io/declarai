import logging

from declarai.python_llm.parsers.function_parser import ParsedFunction
from compilers.output_prompt import compile_output_prompt


INPUTS_TEMPLATE = "Inputs:\n{inputs}\n"
INPUT_LINE_TEMPLATE = "{param}: {{{param}}}"
NEW_LINE_INPUT_LINE_TEMPLATE = "\n{param}: {{{param}}}"


logger = logging.getLogger("generator")


class FunctionLLMTranslator:
    """
    This class is responsible for translating a given function into the components used for
    creating an LLM prompt. The class extracts different parts of the function such as the
    function name, the function arguments, the function docstring, and the function return
    to later create the LLM prompt.
    """

    def __init__(self, parsed_function: ParsedFunction):
        self.parsed_func = parsed_function

    @property
    def has_any_return_defs(self) -> bool:
        return any(
            [
                self.parsed_func.docstring_return[0],
                self.parsed_func.docstring_return[1],
                self.parsed_func.signature_return_type,
            ]
        )

    def compile_input_prompt(self) -> str:
        doc_params = self.parsed_func.docstring_params
        input_prompt = ""
        for (
            signature_arg,
            signature_arg_type,
        ) in self.parsed_func.signature_kwargs.items():
            param_doc = doc_params.get(signature_arg)
            if param_doc:
                input_prompt += (
                    f"{signature_arg}: {signature_arg_type},  # {param_doc}\n"
                )
            else:
                input_prompt += f"{signature_arg}: {signature_arg_type},\n"
        return input_prompt

    def compile_input_placeholder(self) -> str:
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

        for i, param in enumerate(self.parsed_func.signature_kwargs.keys()):
            if i == 0:
                inputs += INPUT_LINE_TEMPLATE.format(param=param)
                continue
            inputs += NEW_LINE_INPUT_LINE_TEMPLATE.format(param=param)

        return INPUTS_TEMPLATE.format(inputs=inputs)

    def compile_output_prompt(self) -> str:
        return_type = self.parsed_func.signature_return_type
        return_name, return_doc = self.parsed_func.docstring_return
        magic_definition = self.parsed_func.magic
        return_name = return_name or magic_definition or "declarai_result"

        if not self.has_any_return_defs:
            logger.warning(
                "Couldn't create output schema for function %s."
                "Falling back to unstructured output."
                "Please add at least one of the following: return type, return doc, return name",
                self.parsed_func.name,
            )
            return ""

        return compile_output_prompt(
            return_type=return_type,
            return_name=return_name,
            return_docstring=return_doc,
            return_magic=magic_definition,
        )
