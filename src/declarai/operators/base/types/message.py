from enum import Enum
from typing_extensions import Self
from pydantic import BaseModel


class MessageRole(str, Enum):
    system = "system"
    user = "user"
    assistant = "assistant"
    function = "function"


class Message(BaseModel):
    message: str
    role: MessageRole

    def __str__(self):
        return self.message

    def __repr__(self):
        return f"{self.role.value}: {self.message}"

    def __eq__(self, other):
        return self.message == other.message and self.role == other.role
