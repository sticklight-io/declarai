# Initialization :beginner:

Although using the docstring and class properties is the recommended way to initialize a chatbot, it is not the only way.
In cases were relying on the class docstring and properties is problematic, we allow manually passing the chat arguments to the class constructor.<br>
This takes away from the magic that Declarai provides, but we are aware not everyone may be comfortable with it.


## Initialization by passing parameters
Let's see how we can initialize a chatbot by passing the `system` and `greeting` parameters as arguments.

```py
@declarai.experimental.chat
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


## Next steps

You are welcome to explore our [**Features**](../../../features/) section, where you can find the full list of supported features and how to use them.