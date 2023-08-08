from typing import List

from .base import ChatMemory
from ..operators.base.types import Message


class PostgresMemory(ChatMemory):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def history(self) -> List[Message]:
        pass

    def add_message(self, message: Message) -> None:
        pass