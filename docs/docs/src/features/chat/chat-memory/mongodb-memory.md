
# MongoDB Memory :material-database:

For chat that requires a persistent and scalable message history, you can use a MongoDB database to store the conversation history.

## Set MongoDB memory

```py
from declarai import Declarai
from declarai.memory import MongoDBMessageHistory
declarai = Declarai(provider="openai", model="gpt-3.5-turbo")

@declarai.experimental.chat(
    chat_history=MongoDBMessageHistory(
        connection_string="mongodb://localhost:27017/mydatabase",
        session_id="unique_chat_id")
) # (1)!
class SQLBot:
    """
    You are a sql assistant. You help with SQL related questions with one-line answers.
    """

sql_bot = SQLBot()
```

1. The `connection_string` parameter specifies the connection details for the MongoDB database. Replace `localhost`, `27017`, and `mydatabase` with your specific MongoDB connection details. The `session_id` parameter uniquely identifies the chat session for which the history is being stored.


## Set MongoDB memory at runtime

In case you want to set the MongoDB memory at runtime, you can use the `set_memory` method.

```py
from declarai import Declarai
from declarai.memory import MongoDBMessageHistory

declarai = Declarai(provider="openai", model="gpt-3.5-turbo")


@declarai.experimental.chat
class SQLBot:
    """
    You are a sql assistant. You help with SQL related questions with one-line answers.
    """


sql_bot = SQLBot(chat_history=MongoDBMessageHistory(connection_string="mongodb://localhost:27017/mydatabase",
                                                   session_id="unique_chat_id"))
```

## Dependencies

Make sure to install the following dependencies before using MongoDB memory.

```bash
pip install declarai[mongodb]
```