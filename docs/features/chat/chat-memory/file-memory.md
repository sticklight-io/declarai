# File Memory :material-file:

For chat that requires a persistent message history, you can use a file to store the conversation history.

## Set file memory

```py
import declarai
from declarai.memory import FileMessageHistory
gpt_35 = declarai.openai(model="gpt-3.5-turbo")

@gpt_35.experimental.chat(chat_history=FileMessageHistory("sql_bot_history.txt")) # (1)!
class SQLBot:
    """
    You are a sql assistant. You help with SQL related questions with one-line answers.
    """

sql_bot = SQLBot()
```


1. file path is not mandatory. If you do not provide a file path, the default file path is stored in a tmp directory.

We can also initialize the `FileMessageHistory` class with a custom file path.


## Set file memory at runtime
In case you want to set the file memory at runtime, you can use the `set_memory` method.

```py
import declarai
from declarai.memory import FileMessageHistory
gpt_35 = declarai.openai(model="gpt-3.5-turbo")

@gpt_35.experimental.chat
class SQLBot:
    """
    You are a sql assistant. You help with SQL related questions with one-line answers.
    """

sql_bot = SQLBot(chat_history=FileMessageHistory("sql_bot_history.txt"))
```
