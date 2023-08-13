
# PostgreSQL Memory :material-database:

For chat that requires a persistent message history with the advantages of scalability and robustness, you can use a PostgreSQL database to store the conversation history.

## Set PostgreSQL memory

```py
from declarai import Declarai
from declarai.memory import PostgresMessageHistory
declarai = Declarai(provider="openai", model="gpt-3.5-turbo")

@declarai.experimental.chat(
    chat_history=PostgresMessageHistory(
        connection_string="postgresql://username:password@localhost:5432/mydatabase",
        session_id="unique_chat_id")
) # (1)!
class SQLBot:
    """
    You are a sql assistant. You help with SQL related questions with one-line answers.
    """

sql_bot = SQLBot()
```

1. The `connection_string` parameter specifies the connection details for the PostgreSQL database. Replace `username`, `password`, `localhost`, `5432`, and `mydatabase` with your specific PostgreSQL connection details. The `session_id` parameter uniquely identifies the chat session for which the history is being stored.


## Set PostgreSQL memory at runtime

In case you want to set the PostgreSQL memory at runtime, you can use the `set_memory` method.

```py
from declarai import Declarai
from declarai.memory import PostgresMessageHistory

declarai = Declarai(provider="openai", model="gpt-3.5-turbo")

@declarai.experimental.chat
class SQLBot:
    """
    You are a sql assistant. You help with SQL related questions with one-line answers.
    """

sql_bot = SQLBot(chat_history=PostgresMessageHistory(connection_string="postgresql://username:password@localhost:5432/mydatabase", session_id="unique_chat_id"))
```

## Dependencies

Make sure to install the following dependencies before using PostgreSQL memory.

```bash
pip install declarai[postgresql]
```