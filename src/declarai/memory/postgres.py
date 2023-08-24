"""
This module contains the PostgresMessageHistory class, which is used to store chat message history in a PostgreSQL database.

"""
import json
import logging
from typing import List, Optional

from ..operators import Message
from .base import BaseChatMessageHistory

logger = logging.getLogger(__name__)

DEFAULT_TABLE_NAME = "message_store"
"A table name for the PostgreSQL database."
DEFAULT_CONNECTION_STRING = "postgresql://postgres:postgres@localhost:5432/postgres"
"A connection string for a PostgreSQL database."


class PostgresMessageHistory(BaseChatMessageHistory):
    """
    Chat message history that stores history in a PostgreSQL database.

    Args:
        session_id: Arbitrary key that is used to store the messages for a single chat session.
        connection_string: Database connection string.
        table_name: Name of the table to use.
    """

    def __init__(
        self,
        session_id: str,
        connection_string: Optional[str] = DEFAULT_CONNECTION_STRING,
        table_name: str = DEFAULT_TABLE_NAME,
    ):
        try:
            import psycopg2  # pylint: disable=import-outside-toplevel
        except ImportError:
            raise ImportError(
                "Cannot import psycopg2."
                "Please install psycopg2 to use PostgresMessageHistory."
            )
        self.conn = psycopg2.connect(connection_string)
        self.cursor = self.conn.cursor()
        self.table_name = table_name
        self.session_id = session_id
        self._initialize_tables()

    def _initialize_tables(self):
        """Initialize the tables if they don't exist."""
        create_table_query = f"""CREATE TABLE IF NOT EXISTS {self.table_name} (
            id SERIAL PRIMARY KEY,
            session_id TEXT NOT NULL,
            message JSONB NOT NULL
        );"""
        self.cursor.execute(create_table_query)
        self.conn.commit()

    @property
    def history(self) -> List[Message]:
        """Retrieve the messages from the database."""
        query = (
            f"SELECT message FROM {self.table_name} WHERE session_id = %s ORDER BY id;"
        )
        self.cursor.execute(query, (self.session_id,))
        rows = self.cursor.fetchall()
        messages = [Message.parse_obj(row[0]) for row in rows]
        return messages

    def add_message(self, message: Message) -> None:
        """Add a message to the database."""
        from psycopg2 import sql

        query = sql.SQL("INSERT INTO {} (session_id, message) VALUES (%s, %s);").format(
            sql.Identifier(self.table_name)
        )
        self.cursor.execute(query, (self.session_id, json.dumps(message.dict())))
        self.conn.commit()

    def clear(self) -> None:
        """Clear session memory from the database."""
        query = f"DELETE FROM {self.table_name} WHERE session_id = %s;"
        self.cursor.execute(query, (self.session_id,))
        self.conn.commit()

    def close(self):
        """Close cursor and connection."""
        self.cursor.close()
        self.conn.close()

    def __del__(self):
        """Destructor to close cursor and connection."""
        if hasattr(self, "cursor"):
            self.cursor.close()
        if hasattr(self, "conn"):
            self.conn.close()
