import logging
from typing import Any

from declarai.python_llm.parsers.function_parser import ParsedFunction
from declarai.templates import APIJsonRoleInstructionTemplate, InstructFunctionTemplate

from .compilers.output_prompt import compile_output_prompt

INPUTS_TEMPLATE = "Inputs:\n{inputs}\n"
INPUT_LINE_TEMPLATE = "{param}: {{{param}}}"
NEW_LINE_INPUT_LINE_TEMPLATE = "\n{param}: {{{param}}}"

logger = logging.getLogger("FunctionLLMTranslator")


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
    def template(self):
        # return (
        #     InstructFunctionTemplate
        #     if not self.has_any_return_defs
        #     else APIJsonRoleInstructionTemplate
        # )
        return InstructFunctionTemplate

    @property
    def has_any_return_defs(self) -> bool:
        """
        A return definition is any of the following:
        - return type annotation
        - return reference in docstring
        - return referenced in magic placeholder  # TODO: Address magic reference as well.
        """
        return any(
            [
                self.parsed_func.docstring_return[0],
                self.parsed_func.docstring_return[1],
                self.parsed_func.signature_return,
            ]
        )

    @property
    def has_structured_return_type(self) -> bool:
        """
        Except for the following types, a dedicated output parsing
        behavior is required to return the expected return type of the task.
        """
        return (
            self.parsed_func.signature_return.name
            and self.parsed_func.signature_return.name
            not in (
                "str",
                "int",
                "float",
                "bool",
            )
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

        if not self.parsed_func.signature_kwargs.keys():
            return inputs

        for i, param in enumerate(self.parsed_func.signature_kwargs.keys()):
            if i == 0:
                inputs += INPUT_LINE_TEMPLATE.format(param=param)
                continue
            inputs += NEW_LINE_INPUT_LINE_TEMPLATE.format(param=param)

        return INPUTS_TEMPLATE.format(inputs=inputs)

    def compile_output_prompt(self) -> str:
        if not self.has_any_return_defs:
            logger.warning(
                "Couldn't create output schema for function %s."
                "Falling back to unstructured output."
                "Please add at least one of the following: return type, return doc, return name",
                self.parsed_func.name,
            )
            return ""

        signature_return = self.parsed_func.signature_return
        return_name, return_doc = self.parsed_func.docstring_return
        return compile_output_prompt(
            return_type=signature_return.str_schema,
            str_schema=return_name,
            return_docstring=return_doc,
            return_magic=self.parsed_func.magic.return_name,
            structured=self.has_structured_return_type,
        )

    @property
    def return_name(self):
        return (
            self.parsed_func.magic.return_name
            or self.parsed_func.docstring_return[0]
            or "declarai_result"
        )

    @property
    def return_type(self) -> Any:
        return self.parsed_func.signature_return.type_
