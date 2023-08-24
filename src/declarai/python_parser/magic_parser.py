import ast
import textwrap


class Magic:
    def __init__(
        self,
        return_name: str = None,
        task_desc: str = "",
        input_desc: dict = {},
        output_desc: str = "",
    ):
        self.return_name = return_name
        self.task_desc = task_desc
        self.input_desc = input_desc
        self.output_desc = output_desc


def extract_magic_args(code) -> Magic:
    # Parse the code into an abstract syntax tree
    code = textwrap.dedent(code)
    tree = ast.parse(code)

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            function_node = node
            break
    else:
        raise ValueError("function not found")

    # Find the magic function call
    for node in ast.walk(function_node):
        if isinstance(node, ast.Call):
            if getattr(node.func, "id", None) == "magic":
                magic_call = node
                break
            if getattr(node.func, "attr", None) == "magic":
                magic_call = node
                break
    else:
        raise ValueError("magic function call not found")

    # Extract the arguments
    if len(magic_call.args) > 0:
        try:
            return_name = magic_call.args[0].s
        except:  # noqa
            return_name = magic_call.args[0].id
    else:
        return_name = None

    task_desc = ""
    input_desc = {}
    output_desc = ""
    for kwarg in magic_call.keywords:
        if kwarg.arg == "task_desc":
            task_desc = kwarg.value.s
        elif kwarg.arg == "input_desc":
            zipped = zip(kwarg.value.keys, kwarg.value.values)
            for k, v in zipped:
                input_desc[k.s] = v.s
        elif kwarg.arg == "output_desc":
            output_desc = kwarg.value.s

    return Magic(
        return_name=return_name,
        task_desc=task_desc,
        input_desc=input_desc,
        output_desc=output_desc,
    )
