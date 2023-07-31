# Chat memory :brain:

Every chat got its own brain. `@declarai.chat` objects saves the conversation history. This is useful when you want to keep the conversation going and have the chatbot remember the context of the conversation.



Let's have a quick conversation with our beloved SQLBot.
```py
from declarai import Declarai

declarai = Declarai(provider="openai", model="gpt-3.5-turbo")


@declarai.chat
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

1. At the first message, the conversation memory is empty, so the chatbot will use the system prompt to generate the response.
2. At the second message, the conversation memory is not empty, it contains the first user message & the chatbot response.
    

## Conversation History

Let's view the conversation history by accessing the `conversation` attribute.

```py
sql_bot.conversation

> [
    user: When should I use a LEFT JOIN?, 
    assistant: You should use a LEFT JOIN when you want to retrieve all records from the left table and matching records from the right table.,
    user: But how is it different from a RIGHT JOIN?,
    assistant: A LEFT JOIN retrieves all records from the left table and matching records from the right table, while a RIGHT JOIN retrieves all records from the right table and matching records from the left table.
]

```

Wow! The chatbot remembers the conversation history.

!!! warning
    
    Keep in mind that the conversation history does not contain the system prompt. It only contains the user messages and the chatbot responses.

If you want to access the system message, you can use the `system` attribute.

```py
sql_bot.system

> "system: You are a sql assistant. You help with SQL related questions with one-line answers.\n"
```


