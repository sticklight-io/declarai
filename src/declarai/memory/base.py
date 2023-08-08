from abc import abstractmethod

from declarai.operators.base.types import Message


class ChatMemory:
    def __init__(self, **kwargs):
        ...

    @abstractmethod
    def history(self):
        pass

    @abstractmethod
    def add_message(self, message: Message) -> None:
        pass
