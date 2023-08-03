# Chat memory :brain:

A chat instance holds the conversation history on a property named `conversation` and uses it across `send` requests.

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

1. The first message is sent with only the previously provided context.
2. The second message addresses the previously conducted conversation when generating it's answer.


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

!!! warning
    
    Keep in mind that the conversation history does not contain the system prompt. It only contains the user messages and the chatbot responses.

If you want to access the system message, you can use the `system` attribute.

```py
sql_bot.system

> "system: You are a sql assistant. You help with SQL related questions with one-line answers.\n"
```

<div style="text-align: right">
    <a href="../controlling-chat-behavior" class="md-button">
        Next <i class="fas fa-arrow-right"></i>
    </a>
</div>
