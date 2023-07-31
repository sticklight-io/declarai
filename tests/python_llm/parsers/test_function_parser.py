from typing import List

from declarai.python_llm.parsers.function_parser import ParsedFunction


def test_output_prompt():
    def my_func(a_param: str, b_param: int) -> List[str]:
        """
        This is the method docstring
        :param a_param: ths param is a string
        :param b_param: this param is an integer
        :return: This returns a list of strings
        """

    parsed_func = ParsedFunction(my_func)
    assert parsed_func.name == "my_func"
    assert parsed_func.signature_kwargs == {"a_param": "str", "b_param": "int"}
    assert parsed_func.signature_return == "List[str]"
    assert parsed_func.docstring_freeform == "This is the method docstring"
    assert parsed_func.docstring_params == {
        "a_param": "ths param is a string",
        "b_param": "this param is an integer",
    }
