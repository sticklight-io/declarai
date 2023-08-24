"""
This module contains the RedisMessageHistory class, which is used to store chat message history in a Redis database.
"""

import json
import logging
from typing import List, Optional

from ..operators import Message
from .base import BaseChatMessageHistory

logger = logging.getLogger(__name__)

DEFAULT_TABLE_NAME = "message_store"
"""A table name for the Redis database."""
DEFAULT_URL = "redis://localhost:6379/0"
"""A URL for the Redis database."""


class RedisMessageHistory(BaseChatMessageHistory):
    """
    Chat message history that stores history in a Redis database.

    Args:
        session_id: Arbitrary key that is used to store the messages for a single chat session.
        url: URL to connect to the Redis server.
        key_prefix: Prefix for the Redis key.
        ttl: Time-to-live for the message records.
    """

    def __init__(
        self,
        session_id: str,
        url: str = DEFAULT_URL,
        key_prefix: str = f"{DEFAULT_TABLE_NAME}:",
        ttl: Optional[int] = None,
    ):
        super().__init__()
        try:
            import redis  # pylint: disable=import-outside-toplevel
        except ImportError:
            raise ImportError(
                "Could not import redis python package. "
                "Please install it with `pip install redis`."
            )

        self.redis_client = redis.StrictRedis.from_url(url)
        self.session_id = session_id
        self.key_prefix = key_prefix
        self.ttl = ttl

    @property
    def key(self) -> str:
        """Construct the record key to use"""
        return self.key_prefix + self.session_id

    @property
    def history(self) -> List[Message]:
        """Retrieve the messages from Redis"""
        _items = self.redis_client.lrange(self.key, 0, -1)
        items = [json.loads(m.decode("utf-8")) for m in _items[::-1]]
        messages = [Message.parse_obj(obj=dict_item) for dict_item in items]
        return messages

    def add_message(self, message: Message) -> None:
        """Append the message to the record in Redis"""
        self.redis_client.lpush(self.key, json.dumps(message.dict()))
        if self.ttl:
            self.redis_client.expire(self.key, self.ttl)

    def clear(self) -> None:
        """Clear session memory from Redis"""
        self.redis_client.delete(self.key)
