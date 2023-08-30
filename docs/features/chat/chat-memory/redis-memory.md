
# Redis Memory :material-database:

For chat that requires a fast and scalable message history, you can use a Redis database to store the conversation history.

## Set Redis memory

```py
import declarai
from declarai.memory import RedisMessageHistory
gpt_35 = declarai.openai(model="gpt-3.5-turbo")

@gpt_35.experimental.chat(
    chat_history=RedisMessageHistory(
        session_id="unique_chat_id",
        url="redis://localhost:6379/0"
    )
) # (1)!
class SQLBot:
    """
    You are a sql assistant. You help with SQL related questions with one-line answers.
    """

sql_bot = SQLBot()
```

1. The `url` parameter specifies the connection details for the Redis server. Replace `localhost` and `6379` with your specific Redis connection details. The `session_id` parameter uniquely identifies the chat session for which the history is being stored.

We can also initialize the `RedisMessageHistory` class with custom connection details.

## Set Redis memory at runtime

In case you want to set the Redis memory at runtime, you can use the `set_memory` method.

```py
import declarai
from declarai.memory import RedisMessageHistory
gpt_35 = declarai.openai(model="gpt-3.5-turbo")

@gpt_35.experimental.chat
class SQLBot:
    """
    You are a sql assistant. You help with SQL related questions with one-line answers.
    """

sql_bot = SQLBot(chat_history=RedisMessageHistory(session_id="unique_chat_id", url="redis://localhost:6379/0"))
```

## Dependencies

Make sure to install the following dependencies before using Redis memory.

```bash
pip install declarai[redis]
```
