# Control LLM params
Language models have various parameters that can be tuned to control the output of the model. To see the parameters for a specific LLM, see the corresponding [provider](../providers/index.md).

Here is an example of how to control these parameters in a declarai task/chat:


## Set at declaration

```python
from declarai import Declarai

declarai = Declarai(provide="openai", model="gpt4", openai_token="<your API key>")

@declarai.task(llm_params={"temperature": 0.5, "max_tokens": 1000})
def generate_song():
    """
    Generate a song about declarai
    """

```

## Set at runtime
We can also pass parameters to the declarai task/chat interface at runtime:

```python
from declarai import Declarai

declarai = Declarai(provide="openai", model="gpt4", openai_token="<your API key>")

@declarai.task
def generate_song():
    """
    Generate a song about declarai
    """

generate_song(llm_params={"temperature": 0.5, "max_tokens": 1000}) # (1)!
```

1. The `llm_params` argument is passed at runtime instead of at declaration.


## Override at runtime
Furthermore, we can pass parameters to the declarai task/chat interface at runtime and override the parameters passed at declaration:

```python
from declarai import Declarai

declarai = Declarai(provide="openai", model="gpt4", openai_token="<your API key>")

@declarai.task(llm_params={"temperature": 0.5, "max_tokens": 1000})
def generate_song():
    """
    Generate a song about declarai
    """

generate_song(llm_params={"temperature": 0.3, "max_tokens": 500})
```

In this case, the `llm_params` argument passed at runtime will override the `llm_params` argument passed at declaration.


## Set for Chat interface
Same as with tasks, we can pass parameters to the declarai chat interface at declaration, at runtime, or override the parameters passed at declaration at runtime.

```python
from declarai import Declarai

declarai = Declarai(provide="openai", model="gpt4", openai_token="<your API key>")

@declarai.experimental.chat(llm_params={"temperature": 0.5, "max_tokens": 1000})
class SQLAdvisor:
    """
    You are a proficient sql adivsor.
    Your goal is to help user's with sql related questions.
    """
```
In the case above, all messages sent to the chat interface will use the parameters passed at declaration.

