from typing import List

from declarai.python_parsers.function_parser import PythonParser, SignatureReturn


def test_output_prompt():
    def my_func(a_param: str, b_param: int) -> List[str]:
        """
        This is the method docstring
        :param a_param: ths param is a string
        :param b_param: this param is an integer
        :return: This returns a list of strings
        """

    parsed_func = PythonParser(my_func)
    assert parsed_func.name == "my_func"
    assert parsed_func.signature_kwargs == {"a_param": str, "b_param": int}
    return_signature = SignatureReturn(
        name="typing.List[str]",
        str_schema="List[string]",
        type_=List[str],
    )
    assert parsed_func.signature_return.name == return_signature.name
    assert parsed_func.signature_return.str_schema == return_signature.str_schema
    assert parsed_func.signature_return.type_ == return_signature.type_
    assert parsed_func.docstring_freeform == "This is the method docstring"
    assert parsed_func.docstring_params == {
        "a_param": "ths param is a string",
        "b_param": "this param is an integer",
    }
