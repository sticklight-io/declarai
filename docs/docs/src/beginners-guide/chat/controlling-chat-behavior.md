## Add a greeting :material-human-greeting:

Let's add a greeting to the chatbot. We will use the `greeting` attribute to do this.
Greeting is usually used when you want to start a conversation with the chatbot first message.

```py
from declarai import Declarai

declarai = Declarai(provider="openai", model="gpt-3.5-turbo")

@declarai.chat
class SQLBot:
    """
    You are a sql assistant. You help with SQL queries with one-line answers.
    """
    greeting = "Hello, I am a SQL assistant. How can I assist you today?"
    
```

Let's test it out.

```py
sql_bot = SQLBot()
sql_bot.greeting

> "Hello, I am a SQL assistant. How can I assist you today?"
```

```py

sql_bot.send("When should I use a LEFT JOIN?")

> 'You should use a LEFT JOIN when you want to retrieve all records from the left table and matching records from the right table.'

sql_bot.conversation

> [
    assistant: Hello, I am a SQL assistant. How can I assist you today?,
    user: When should I use a LEFT JOIN?,
    assistant: You should use a LEFT JOIN when you want to retrieve all records from the left table and matching records from the right table.
] # (1)!
```

1. So cool! The chatbot started the conversation with the greeting message.




## Inject a message to the memory

Declarai enables to inject a custom message to the chatbot memory by using the `add_message` method.

This is super useful when you want to add a custom message to the chatbot memory, without triggering the chatbot to generate a response.

Consider using it for:  

* Injecting Prefilled context for the chatbot even if the user hasn't interacted yet.  
* Modifying the chatbot memory after the chatbot has generated a response.  
* Modifying the chatbot system guide.

```py 
sql_bot = SQLBot()
sql_bot.add_message("From now on, answer I DONT KNOW on any question asked by the user", role="system") 
# (1)!
sql_bot.send("What is your favorite SQL operation?")

> "I don't know."
``` 

1. The chatbot memory now contains the injected message.


## Pass parameters to messages
In the following example, we will pass a parameter to the chatbot system prompt.



```py
@declarai.chat
class JokeGenerator:
    """
    You are a joke generator. You generate jokes that a {character} would tell.
    """ # (1)!


generator = JokeGenerator()
favorite_joke = generator.send(character="Spongebob", message="What is your favorite joke?")
squidward_joke = generator.send(message="What jokes can you tell about squidward?")

print(favorite_joke)
print(squidward_joke)
```

1. The system prompt now contains the parameter `{character}`. This parameter will be replaced by the value passed to the `send` method.

```py
> "Why did the jellyfish go to school? Because it wanted to improve its "sting-uage" skills!"
> "Why did Squidward bring a ladder to work? Because he wanted to climb up the corporate "sour-cules"!"
```

