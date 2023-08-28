# Customizing the Chat Response

The default response type of the language model messages is `str`. However, you can overwrite the `send` method to return a different type.<br>
Just like tasks, you can control the type hints by declaring the return type of the `send` method.

```py
from typing import List
import declarai
openai = declarai.openai(model="gpt-3.5-turbo")

@openai.experimental.chat
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

!!! warning

     As with tasks, the message is sent along with the expected return types.
     This means that if not careful, a message conflicting with the expected results could cause weird behavior in the llm responses.<br>
     For more best-practices, see [here](../../../best-practices).
