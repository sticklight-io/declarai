from abc import abstractmethod, ABC

from declarai.operators.base.types import Message


class BaseChatMessageHistory(ABC):
    """
    Abstract class to store the chat message history.

    See `ChatMessageHistory` for default implementation.

    """
    @property
    @abstractmethod
    def history(self):
        """Return the chat message history"""
        pass

    @abstractmethod
    def add_message(self, message: Message) -> None:
        """Add a Message object to the state."""
        pass

    @abstractmethod
    def clear(self) -> None:
        """Remove all messages from the state"""
