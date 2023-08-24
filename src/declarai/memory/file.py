"""
This module contains the FileMessageHistory class, which is used to store chat message history in a local file.
"""
import json
import logging
import tempfile
from pathlib import Path
from typing import Dict, List, Optional

from ..operators import Message
from .base import BaseChatMessageHistory

logger = logging.getLogger(__name__)


class FileMessageHistory(BaseChatMessageHistory):
    """
    Chat message history that stores history in a local file.

    Args:
        file_path: path of the local file to store the messages. if not passed the messages will be stored in a temporary file,
         and a warning will be logged.
    """

    def __init__(self, file_path: Optional[str] = None):
        super().__init__()
        if not file_path:
            # Create a temporary file and immediately close it to get its name.
            temp = tempfile.NamedTemporaryFile(delete=False)
            self.file_path = Path(temp.name)
            self.file_path.write_text(json.dumps([]))
            logger.warning(
                "No file path provided to store the messages. "
                f"Messages will be stored in a temporary file path: {self.file_path}"
            )
        else:
            self.file_path = Path(file_path)

        if not self.file_path.exists():
            self.file_path.touch()
            self.file_path.write_text(json.dumps([]))

    @property
    def history(self) -> List[Message]:
        """Retrieve the messages from the local file"""
        items: List[Dict] = json.loads(self.file_path.read_text())
        messages = [Message.parse_obj(obj=dict_item) for dict_item in items]
        return messages

    def add_message(self, message: Message) -> None:
        """Append the message to the record in the local file"""
        messages = self.history.copy()
        messages.append(message)
        messages_dict = [msg.dict() for msg in messages]
        self.file_path.write_text(json.dumps(messages_dict))

    def clear(self) -> None:
        """Clear session memory from the local file"""
        self.file_path.write_text(json.dumps([]))
