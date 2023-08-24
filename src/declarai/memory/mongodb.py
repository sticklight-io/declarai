"""
This module contains the MongoDBMessageHistory class, which is used to store chat message history in a MongoDB database.

"""
import json
import logging
from typing import List

from ..operators import Message
from .base import BaseChatMessageHistory

logger = logging.getLogger(__name__)

DEFAULT_DBNAME = "chat_history"
"""A database name for the MongoDB database."""
DEFAULT_COLLECTION_NAME = "message_store"
"""A collection name for the MongoDB database."""
DEFAULT_CONNECTION_STRING = "mongodb://localhost:27017"
"""A connection string for a MongoDB database."""


class MongoDBMessageHistory(BaseChatMessageHistory):
    """
    Chat message history that stores history in MongoDB.

    Args:
        connection_string: connection string to connect to MongoDB
        session_id: Arbitrary key that is used to store the messages for a single chat session.
        database_name: name of the database to use
        collection_name: name of the collection to use
    """

    def __init__(
        self,
        session_id: str,
        connection_string: str = DEFAULT_CONNECTION_STRING,
        database_name: str = DEFAULT_DBNAME,
        collection_name: str = DEFAULT_COLLECTION_NAME,
    ):
        try:
            from pymongo import MongoClient
        except ImportError:
            raise ImportError(
                "Could not import pymongo python package. "
                "Please install it with `pip install pymongo`."
            )

        self.connection_string = connection_string
        self.session_id = session_id
        self.database_name = database_name
        self.collection_name = collection_name

        self.client: MongoClient = MongoClient(connection_string)
        self.db = self.client[database_name]
        self.collection = self.db[collection_name]
        self.collection.create_index("SessionId")

    @property
    def history(self) -> List[Message]:
        """Retrieve the messages from MongoDB"""
        cursor = self.collection.find({"SessionId": self.session_id})

        if cursor:
            items = [json.loads(document["History"]) for document in cursor]
        else:
            items = []

        messages = [Message.parse_obj(obj=dict_item) for dict_item in items]
        return messages

    def add_message(self, message: Message) -> None:
        """Append the message to the record in MongoDB"""
        self.collection.insert_one(
            {
                "SessionId": self.session_id,
                "History": json.dumps(message.dict()),
            }
        )

    def clear(self) -> None:
        """Clear session memory from MongoDB"""
        self.collection.delete_many({"SessionId": self.session_id})
