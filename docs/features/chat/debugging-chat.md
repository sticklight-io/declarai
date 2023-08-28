# Debugging Chat :bug:

Similarly to debugging tasks, understanding the prompts being sent to the llm is crucial to debugging chatbots.
Declarai exposes the `compile` method for chat instances as well!

## Compiling chat
```py
import declarai
openai = declarai.openai(model="gpt-3.5-turbo")

@openai.experimental.chat
class SQLBot:
    """
    You are a sql assistant. You help with SQL queries with one-line answers.
    """
    greeting = "Hello, I am a SQL assistant. How can I assist you today?"

sql_bot = SQLBot()
print(sql_bot.compile())
```
```py
> {
    'messages': 
        [
            "system: You are a sql assistant. You help with SQL queries with one-line answers.", 
            "assistant: Hello, I am a SQL assistant. How can I assist you today?"
        ]
}
```
Wonderful right? We can view the chatbot's messages in the format they will be sent to the language model.
