from declarai.operators import OpenAILLM, OpenAIChatOperator
from declarai.python_parser.parser import PythonParser


def test_chat_openai_operator():
    openai_operator_class = OpenAIChatOperator
    llm = OpenAILLM(
        openai_token="test-token",
        model="test-model",
    )

    class MyChat:
        """
        This is my beloved chat
        """

    parsed = PythonParser(MyChat)
    openai_operator_instance = openai_operator_class(parsed=parsed, llm=llm)
    assert openai_operator_instance.parsed.name == MyChat.__name__
    compiled = openai_operator_instance.compile(messages=[])
    assert isinstance(compiled, dict)
    messages = list(compiled["messages"])
    assert len(messages) == 1
    assert messages[0].message == "This is my beloved chat"
    assert messages[0].role == "system"

    # def openai_task():
    #     ...
    #
    # parsed = PythonParser(openai_task)
    # openai_operator_instance = openai_operator_class(parsed=parsed, llm=llm)
    # assert openai_operator_instance.parsed.name == openai_task.__name__
    # compiled = openai_operator_instance.compile()
    # assert isinstance(compiled, dict)
    # messages = list(compiled["messages"])
    # assert len(messages) == 1
    # assert messages[0].message == "\n\n"
    # assert messages[0].role == "user"
