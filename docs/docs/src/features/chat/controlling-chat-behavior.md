## Greetings :material-human-greeting:

Greetings are used to start the conversation with a bot message instead of a user message.
The `greeting` attribute defines this first message and is added to the conversation on initialization.

```py
@declarai.experimental.chat
class SQLBot:
    """
    You are a sql assistant. You help with SQL queries with one-line answers.
    """
    greeting = "Hello, I am a SQL assistant. How can I assist you today?"
```

The greeting attribute is later available as a property of the chatbot instance to use when implementing your interface.
```py
sql_bot = SQLBot()
sql_bot.greeting

> "Hello, I am a SQL assistant. How can I assist you today?"
```

```py

sql_bot.send("When should I use a LEFT JOIN?")

> 'You should use a LEFT JOIN when you want to retrieve all records from the left table and matching records from the right table.'

sql_bot.conversation

> [ # (1)!
    assistant: Hello, I am a SQL assistant. How can I assist you today?,
    user: When should I use a LEFT JOIN?,
    assistant: You should use a LEFT JOIN when you want to retrieve all records from the left table and matching records from the right table.
] 
```

1. We can see here that the greeting, initiated by the assistant, is the first message in the conversation.

## Inject a message to the memory

Declarai enables injecting custom messages into the conversation history by using the `add_message` method.

This is super useful when you want to intervene with the conversation flow without necessarily triggering another response from the model.

Consider using it for:  

* Creating a prefilled conversation even before the user's interaction.  
* Modifying the chatbot memory after the chatbot has generated a response.  
* Modifying the chatbot system prompt.
* Guiding the conversation flow given certain criteria met in the user-bot interaction.

```py 
sql_bot = SQLBot()
sql_bot.add_message("From now on, answer I DONT KNOW on any question asked by the user", role="system") 
# (1)!
sql_bot.send("What is your favorite SQL operation?")

> "I don't know."
``` 

1. The chatbot's conversation history now contains the injected message and reacts accordingly.


## Dynamic system prompting
In the following example, we will pass a parameter to the chatbot system prompt.
This value will be populated at runtime and will allow us to easily create base chatbots with varying behaviors.

```py
@declarai.experimental.chat
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