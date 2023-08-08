from typing import Optional, List

from .base import ChatMemory
from declarai.operators.base.types import Message


class InMemory(ChatMemory):
    """
    This memory implementation stores all messages in memory in a list.
    """

    def __init__(self, messages: Optional[List[Message]] = None, **kwargs):
        super().__init__(**kwargs)
        self.messages = messages or []

    def history(self) -> List[Message]:
        """
        Returns the list of messages stored in memory.
        :return: List of messages
        """
        return self.messages

    def add_message(self, message: Message) -> None:
        """
        Adds a message to the list of messages stored in memory.
        :param message: the message content and role
        """
        self.messages.append(message)
