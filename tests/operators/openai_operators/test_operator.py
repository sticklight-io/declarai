from declarai.operators import OpenAITaskOperator
from declarai.python_parser.parser import PythonParser


def test_openai_operator():
    openai_operator_class = OpenAITaskOperator.new_operator(
        openai_token="test-token",
        model="test-model",
    )

    def openai_task(argument: str) -> str:
        """
        This is a test task
        :param argument: this is a test argument
        :return: this is a test return
        """

    parsed = PythonParser(openai_task)
    openai_operator_instance = openai_operator_class(parsed)
    assert openai_operator_instance.parsed.name == openai_task.__name__
    compiled = openai_operator_instance.compile()
    assert isinstance(compiled, dict)
    messages = list(compiled["messages"])
    assert len(messages) == 1
    assert (
        messages[0].message == "This is a test task\nInputs:\nargument: {argument}\n\n"
    )
    assert messages[0].role == "user"

    def openai_task():
        ...

    parsed = PythonParser(openai_task)
    openai_operator_instance = openai_operator_class(parsed)
    assert openai_operator_instance.parsed.name == openai_task.__name__
    compiled = openai_operator_instance.compile()
    assert isinstance(compiled, dict)
    messages = list(compiled["messages"])
    assert len(messages) == 1
    assert messages[0].message == "\n\n"
    assert messages[0].role == "user"
