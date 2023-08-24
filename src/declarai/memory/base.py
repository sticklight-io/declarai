"""
Base class for the memory module.
"""
from abc import ABC, abstractmethod  # pylint: disable=E0611
from typing import List

from declarai.operators import Message


class BaseChatMessageHistory(ABC):
    """
    Abstract class to store the chat message history.

    See `ChatMessageHistory` for default implementation.

    """

    @property
    @abstractmethod
    def history(self) -> List[Message]:
        """
        Return the chat message history

        Returns:
            List of Message objects
        """

    @abstractmethod
    def add_message(self, message: Message) -> None:
        """
        Add a Message object to the state.

        Args:
            message: Message object to add to the state
        """

    @abstractmethod
    def clear(self) -> None:
        """
        Remove all messages from the state
        """
