# Chat memory :brain:

A chat instance saves the message history and uses it to future responses.
Here is an example of a chatbot that retains conversation history across multiple `send` requests.
```py
@declarai.experimental.chat
class SQLBot:
    """
    You are a sql assistant. You help with SQL related questions with one-line answers.
    """

sql_bot = SQLBot()

sql_bot.send("When should I use a LEFT JOIN?") # (1)!
> "You should use a LEFT JOIN when you want to retrieve all records from the left table and matching records from the right table."

sql_bot.send("But how is it different from a RIGHT JOIN?") # (2)!
> "A LEFT JOIN retrieves all records from the left table and matching records from the right table, while a RIGHT JOIN retrieves all records from the right table and matching records from the left table."
```

1. The first message is sent with the system prompt.
2. The second message is sent with the previous conversation and therefore the model is aware of the first question.


## Conversation History
You can view the conversation history by accessing the `conversation` attribute.

```py
sql_bot.conversation

> [
    user: When should I use a LEFT JOIN?, 
    assistant: You should use a LEFT JOIN when you want to retrieve all records from the left table and matching records from the right table.,
    user: But how is it different from a RIGHT JOIN?,
    assistant: A LEFT JOIN retrieves all records from the left table and matching records from the right table, while a RIGHT JOIN retrieves all records from the right table and matching records from the left table.
]

```

!!! warning
    
    Keep in mind that the conversation history does not contain the system prompt. It only contains the user messages and the chatbot responses.

If you want to access the system message, you can use the `system` attribute.

```py
sql_bot.system

> "system: You are a sql assistant. You help with SQL related questions with one-line answers.\n"
```


## Default Memory

**The default message history of a chat is a simple in-memory list**. This means that history exists only for the duration of the chatbot session.

If you prefer to have a persistent history, you can use the `FileMessageHistory` class from the `declarai.memory` module.


## Setting up a memory
Setting up a memory is done by passing `chat_history` as a keyword argument to the `declarai.experimental.chat` decorator.

```py
from declarai import Declarai
from declarai.memory import FileMessageHistory

declarai = Declarai(provider="openai", model="gpt-3.5-turbo")

@declarai.experimental.chat(chat_history=FileMessageHistory("sql_bot_history.txt")) # (1)!
class SQLBot:
    """
    You are a sql assistant. You help with SQL related questions with one-line answers.
    """
```

1. file path is not mandatory. If you do not provide a file path, the default file path is stored in a tmp directory.

We can also initialize the chat_history at runtime

```py
from declarai import Declarai
from declarai.memory import FileMessageHistory

declarai = Declarai(provider="openai", model="gpt-3.5-turbo")

@declarai.experimental.chat
class SQLBot:
    """
    You are a sql assistant. You help with SQL related questions with one-line answers.
    """
sql_bot = SQLBot(chat_history=FileMessageHistory("sql_bot_history.txt"))
```
