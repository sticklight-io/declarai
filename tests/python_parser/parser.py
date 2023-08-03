from declarai.python_parser.parser import PythonParser


def test_parser():
    class TestClass:
        pass

    def my_func():
        pass

    # parsed_class = PythonParser(TestClass)
    parsed_func = PythonParser(my_func)
