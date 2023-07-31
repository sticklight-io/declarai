# Debugging Chat :bug:

What is more frustrating than a chatbot that doesn't work? A chatbot that doesn't work and you don't know why.

Declarai makes it **super easy** to debug your chatbot.

Just like tasks, you can debug your chatbot by using the `compile` method.

## Compiling chat
```py
@declarai.chat
class SQLBot:
    """
    You are a sql assistant. You help with SQL queries with one-line answers.
    """
    greeting = "Hello, I am a SQL assistant. How can I assist you today?"

sql_bot = SQLBot()
print(sql_bot.compile())
```
```py
> [
    system: You are a sql assistant. You help with SQL queries with one-line answers.,
    assistant: Hello, I am a SQL assistant. How can I assist you today?, assistant: Hello, I am a SQL assistant. How can I assist you today?
]
```
Wonderful right? We can view the chatbot's messages that will sent to the language model.

## Compiling the next message

Next step in chatbot debugging is to see the next message that will be sent to the language model.

Let's compile the prompt with the next message.

```py
@declarai.chat
class SQLBot:
    """
    You are a sql assistant. You help with SQL queries with one-line answers.
    """
    greeting = "Hello, I am a SQL assistant. How can I assist you today?"

sql_bot = SQLBot()
print(sql_bot.compile(message="Tell me your preferred SQL operation"))
```
```py
> [  
    system: You are a sql assistant. You help with SQL queries with one-line answers.,
    assistant: Hello, I am a SQL assistant. How can I assist you today?,
    user: Tell me your preferred SQL operation
] # (1)!
```

1. The chatbot's next message is now included in the compiled prompt :exploding_head:.

## Compiling to prompt
You can also compile the prompt string that will be sent to the language model by passing `return_prompt=True` 

```py
@declarai.chat
class SQLBot:
    """
    You are a sql assistant. You help with SQL queries with one-line answers.
    """
    greeting = "Hello, I am a SQL assistant. How can I assist you today?"

sql_bot = SQLBot()
print(sql_bot.compile(return_prompt=True, message="Tell me your preferred SQL operation"))
```
```py

> """
system: You are a sql assistant. You help with SQL queries with one-line answers.

assistant: Hello, I am a SQL assistant. How can I assist you today?
user: Tell me your preferred SQL operation
"""
```

!!! tip

    Compiling to prompt is useful when you want to copy/paste the prompt to a language model on your own.
