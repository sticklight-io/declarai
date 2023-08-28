# Multiple models / Multiple providers

Declarai allows you to use multiple models from different providers in the same project.
All you need to do is configure seperate Declarai instances for each model and provider.

```python
import declarai

# Configure the first Declarai instance
declarai_gpt35 = declarai.openai(model="gpt-3.5-turbo")

# Configure the second Declarai instance
declarai_gpt4 = declarai.openai(model="gpt-4")

# Now use the instances to create tasks
@declarai_gpt35.task
def say_something() -> str:
    """
    Say something short to the world
    """
    
@declarai_gpt4.task
def say_something() -> str:
    """
    Say something short to the world
    """

```
