from typing import Optional, TextIO, List
from pathlib import Path
import tempfile
from .base import ChatMemory
from ..operators.base.types import Message
import json

class FileMemory(ChatMemory):
    def __init__(self, filename: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        if filename:
            self.filename = Path(filename)
            if self.filename.suffix.lower() != ".json":
                self.filename = self.filename.with_suffix(".json")
        else:
            # Create a temporary file and immediately close it to get its name.
            temp = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
            self.filename = Path(temp.name)
            temp.close()

    def __read_file(self) -> List[dict]:
        if not self.filename.exists():
            return []
        with open(self.filename, "r") as file:
            return json.load(file)

    def __append_to_file(self, content: dict) -> None:
        data = self.__read_file()
        data.append(content)
        with open(self.filename, "w") as file:
            json.dump(data, file)

    def history(self) -> List[Message]:
        file_content = self.__read_file()
        return [Message.parse_obj(obj=dict_item) for dict_item in file_content]

    def add_message(self, message: Message) -> None:
        self.__append_to_file(message.dict())

