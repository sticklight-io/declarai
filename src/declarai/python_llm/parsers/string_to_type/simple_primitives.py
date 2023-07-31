import typing

from pydantic.tools import parse_raw_as
from typing import Dict

parse_raw_as(Dict[str, str], '{"a": "b"}')
