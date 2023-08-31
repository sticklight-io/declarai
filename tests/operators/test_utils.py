from declarai.operators.utils import can_be_jinja, format_prompt_msg


# Tests for can_be_jinja function
def test_can_be_jinja_valid():
    assert can_be_jinja("Hello {{ name }}") == True


def test_can_be_jinja_invalid():
    assert can_be_jinja("Hello {{ name") == False


def test_can_be_jinja_no_jinja_syntax():
    assert can_be_jinja("Hello name") == False


# Tests for format_prompt_msg function
def test_format_prompt_msg_valid_jinja():
    assert format_prompt_msg("Hello {{ name }}", name="John") == "Hello John"


def test_format_prompt_msg_invalid_jinja():
    assert format_prompt_msg("Hello {{ name", name="John") == "Hello { name"


def test_format_prompt_msg_python_format():
    assert format_prompt_msg("Hello {name}", name="John") == "Hello John"


def test_format_prompt_msg_no_format():
    assert format_prompt_msg("Hello name") == "Hello name"
