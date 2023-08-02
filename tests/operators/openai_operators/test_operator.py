from declarai.operators import OpenAIOperator
from declarai.python_parser.parser import PythonParser


def test_openai_operator():
    openai_operator_class = OpenAIOperator.new_operator(
        openai_token="test-token",
        model="test-model",
    )

    def open_ai_task(argument: str) -> str:
        """
        This is a test task
        :param argument: this is a test argument
        :return: this is a test return
        """

    parsed = PythonParser(open_ai_task)
    openai_operator_instance = openai_operator_class(parsed)
    assert openai_operator_instance.parsed.name == open_ai_task.__name__
    compiled = openai_operator_instance.compile()
    assert isinstance(compiled, list)
    assert len(compiled) == 1
    assert (
        compiled[0].message == "This is a test task\nInputs:\nargument: {argument}\n\n"
    )
    assert compiled[0].role == "user"
