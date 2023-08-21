"""
Message definition for the operators.
"""
from enum import Enum

from pydantic import BaseModel


class MessageRole(str, Enum):
    """
    Message role enum for the Message class to indicate the role of the message in the chat.

    Attributes:
        system: The message is the system message, usually used as the first message in the chat.
        user: Every message that is sent by the user.
        assistant: Every message that is sent by the assistant.
        function: Every message that is sent by the assistant that is a function call.
    """

    system: str = "system"
    user: str = "user"
    assistant: str = "assistant"
    function: str = "function"


class Message(BaseModel):
    """
    Represents a message in the chat.

    Args:
        message: The message string
        role: The role of the message in the chat

    Attributes:
        message: The message string
        role: The role of the message in the chat
    """

    message: str
    role: MessageRole

    def __str__(self):
        return self.message

    def __repr__(self):
        return f"{self.role.value}: {self.message}"

    def __eq__(self, other):
        return self.message == other.message and self.role == other.role
