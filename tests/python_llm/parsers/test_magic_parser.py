import inspect
from unittest.mock import MagicMock

from declarai.python_llm.magic_parser import extract_magic_args, Magic


magic = MagicMock()


def test_magic_parser():
    """
    TODO: This doesn't currently support aliases in the magic function, only string literals
    """

    def mock_magic_parser_function(arg: str):
        return magic(
            "return_name",
            task_desc="This is a task description",
            input_desc={"arg": "This is an argument desc"},
            output_desc="This is an output desc",
            arg=arg,
        )

    code = inspect.getsource(mock_magic_parser_function)
    _magic = extract_magic_args(code)

    assert isinstance(_magic, Magic)
    assert _magic.return_name == "return_name"
    assert _magic.task_desc == "This is a task description"
    assert _magic.input_desc == {"arg": "This is an argument desc"}
    assert _magic.output_desc == "This is an output desc"
