# Initialization :beginner:

We have already seen how to initialize a chatbot in the [Chat Page](/src/beginners-guide/chat) section, using class docstring.


## Initialization by passing parameters
Let's see how we can initialize a chatbot by passing the `system` and `greeting` as arguments.

```py
@declarai.chat
class SQLBot:
    ...


sql_bot = SQLBot(
    system="You are a sql assistant. You help with SQL queries with one-line answers.",
    greeting="Hello, I am a SQL assistant. How can I assist you today?",
)

print(sql_bot.send("Tell me your preferred SQL operation"))
```

```py
> "As an SQL assistant, I don't have a preferred SQL operation. I am here to assist with any SQL operation you need help with."
```

!!! tip
    We recommend using the docstring method for initializing your chatbot. It is more readable.
    However, if you prefer to pass the parameters as arguments, you can do so as well.


## Overwriting the send method

The default response type of the language model messages is `str`. However, you can overwrite the `send` method to return a different type.
Just like tasks, you can control the type hints by declaring the return type of the `send` method.

```py
from typing import List

@declarai.chat
class SQLBot:
    """
    You are a sql assistant."""
    ...
    
    def send(self, operation: str) -> List[str]:
        ...

sql_bot = SQLBot()
print(sql_bot.send(message="Offer two sql queries that use the 'SELECT' operation"))
> [
    "SELECT * FROM table_name;",
    "SELECT column_name FROM table_name;"
]
```