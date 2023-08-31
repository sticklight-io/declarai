# Chatbots :speech_balloon:

Unlike tasks, chatbots are meant to keep the conversation going. <br>
Instead of executing a single operation, they are built to manage conversation context over time.

Declarai can be used to create chatbots. The simplest way to do this is to use the `@declarai.experimental.chat` decorator.

We declare a "system prompt" in the docstring of the class definition.<br>
The system prompt is the initial command that instructs the bot on who they are and what's expected in the conversation. 


```py
import declarai
gpt_35 = declarai.openai(model="gpt-3.5-turbo")

@gpt_35.experimental.chat
class SQLBot:
    """
    You are a sql assistant. You help with SQL related questions 
    """ # (1)!
```

1. The docstring represents the chatbot's description and is used to generate the prompt.

```py
sql_bot = SQLBot()
sql_bot.send("When should I use a LEFT JOIN?") # (1)!

> "You should use a LEFT JOIN when you want to return all rows from the left table, and the matched rows from the right table."
```

1. The created bot exposes a `send` method, by which you can interact and send messages.
    Every call to send results with a response from the bot.


!!! tip
    You can also declare the chatbot system prompt by doing the following
    ```py
    @declarai.experimental.chat
    class SQLBot:
        pass
    sql_bot = SQLBot(system="You are a sql assistant. You help with SQL related questions with one-line answers.")
    ```
