import re

from declarai.python_parser.docstring_parsers.types import BaseDocStringParser
from declarai.python_parser.types import (
    DocstringFreeform,
    DocstringParams,
    DocstringReturn,
)

reST_PARAM_KEY: str = ":param"
reST_RETURN_KEY: str = ":return"
reST_FREEFORM_REGEX = rf"(?s)(.*?)(?=\n{reST_PARAM_KEY}|\n{reST_RETURN_KEY}|$)"
reST_PARAMS_REGEX = (
    rf"(?s)({reST_PARAM_KEY} .*?: .*?)(?=\n{reST_PARAM_KEY}|\n{reST_RETURN_KEY}|$)"
)
reST_RETURN_REGEX = rf"(?s)({reST_RETURN_KEY}: .*?)($)"


class ReSTDocstringParser(BaseDocStringParser):
    """
    As recommended by (PEP 287)[https://peps.python.org/pep-0287/],
    the recommended docstring format is the reStructuredText format (shortform - reST).
    """

    def __init__(self, docstring: str):
        self.docstring = docstring

    @property
    def freeform(self) -> DocstringFreeform:
        if not self.docstring:
            return ""
        freeform = re.search(reST_FREEFORM_REGEX, self.docstring).group().strip()
        return freeform

    @property
    def params(self) -> DocstringParams:
        params = [
            param.group().strip()
            for param in re.finditer(reST_PARAMS_REGEX, self.docstring)
        ]
        params_dict = {}
        for param in params:
            param = param.replace(reST_PARAM_KEY, "").strip()
            param_name, doc = param.split(":")
            params_dict[param_name] = doc.strip()
        return params_dict

    @property
    def returns(self) -> DocstringReturn:
        if not self.docstring:
            return "", ""
        matched_returns = re.search(reST_RETURN_REGEX, self.docstring)
        if matched_returns:
            returns = matched_returns.group().strip()
            returns = returns.replace(reST_RETURN_KEY, "").strip()
            return_name, return_doc = returns.split(":")
            return return_name, return_doc.strip()

        return "", ""
