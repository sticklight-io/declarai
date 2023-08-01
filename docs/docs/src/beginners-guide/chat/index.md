# Chatbots :simple-rocketdotchat:

Unlike tasks, chatbots are meant to keep the conversation going. They are not meant to be executed once and return a result. Instead, they are meant to be used in a loop, where the user can keep asking questions and the chatbot keeps answering them.


Declarai can be used to create chatbots. The simplest way to do this is to use the `@declarai.chat` decorator.

We declare the system prompt in the docstring of the class definition. The system prompt is the prompt that is used to guide the chatbot in the conversation. 


```py
from declarai import Declarai
declarai = Declarai(provider="openai", model="gpt-3.5-turbo")

@declarai.chat
class SQLBot:
    """
    You are a sql assistant. You help with SQL related questions 
    """ # (1)!
```

1. The docstring represents the chatbot's description and is used to generate the prompt.


!!! tip
    You can also declare the chatbot system prompt by doing the following
    ```py
    @declarai.chat
    class SQLBot:
        pass
    sql_bot = SQLBot(system="You are a sql assistant. You help with SQL related questions with one-line answers.")
    ```

```py
sql_bot = SQLBot()
sql_bot.send("When should I use a LEFT JOIN?")

> "You should use a LEFT JOIN when you want to return all rows from the left table, and the matched rows from the right table."
```


!!! note
    Remember, the system prompt is the docstring provided in the class definition.


<div style="text-align: right">
    <a href="../chat/controlling-chat-behavior" class="md-button">
        Next <i class="fas fa-arrow-right"></i>
    </a>
</div>


