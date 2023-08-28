---
hide:
  - footer
---

# Debugging tasks

So it all seems pretty magical up to this point, but what if you want to see what's going on behind the scenes?
Being able to debug your tasks is a very important part of the development process, and **Declarai** makes it easy for you.

## Compiling tasks
The first and simplest tool to better understand what's happening under the hood is the `compile` method.<br>
Declarai has an `evals` module as well for advanced debugging and benchmarking which you can review later here: [evals](../../features/evals/)

Let's take the last task from the previous section and add a call to the `compile` method:
```python
from typing import Dict
import declarai

openai = declarai.openai(model="gpt-3.5-turbo")

@openai.task
def movie_recommender(user_input: str) -> Dict[str, str]:
    """
    Recommend a selection of movies to watch based on the user input
    For each movie provide a short description as well
    :param user_input: The user's input
    :return: A dictionary of movie names and descriptions
    """

movie_recommender.compile()

> {
    'messages': [ # (1)!
        # (2)!        
        system: You are a REST api endpoint. 
                You only answer in JSON structures with a single key named 'declarai_result', nothing else. 
                The expected format is: "declarai_result": Dict[string, string]  # A dictionary of movie names and descriptions,
        # (3)!
        user: Recommend a selection of movies to watch based on the user input  
              For each movie provide a short description as well.
              Inputs: user_input: {user_input} # (4)!
    ]
}
```

1. As we are working with the openai llm provider, which exposes a chat interface, we translate the task into **messages** as defined by openai's API.
2. In order to guide the task with the correct output format, we provide a **system** message that explains LLM's role and expected responses
3. The **user message** is the actual translation of the task at hand, with the user's input as a placeholder for the actual value.
4. **{user_input}** will be populated with the actual value when the task is being called at runtime.

What we're seeing here is the template for this specific task. It is built so that when called at runtime, 
it will be populated with the real values passed to our task.

!!! warning

     As you can see, that the actual prompt being sent to the model is a bit different than the original docstring.
     Even though Declarai incorporates best practices for prompt engineering while maintaining as little interference as possible with user prompts, 
     it is still possible that the model will not generate the desired output. For this reason it is important to be able to debug your tasks and understand what actually got sent to the model

## Compiling tasks with real values
The `compile` method can also be used to view the prompt with the real values provided to the task.
This is useful when prompts might behave differently for different inputs.

```python hl_lines="10"
print(movie_recommender.compile(user_input="I want to watch a movie about space"))

> {
    'messages': [     
        system: You are a REST api endpoint. 
                You only answer in JSON structures with a single key named 'declarai_result', nothing else. 
                The expected format is: "declarai_result": Dict[string, string]  # A dictionary of movie names and descriptions,
        user: Recommend a selection of movies to watch based on the user input  
              For each movie provide a short description as well.
              Inputs: user_input: I want to watch a movie about space # (1)!
]}
```

1. The actual **value** of the parameter is now populated in the placeholder and we have our final prompt!


!!! tip

     With the `compile` method, you can always take your prompts anywhere you like, 
     if it's for monitoring, debugging or just for documentation, we've got you covered!


<div style="display: flex; justify-content: space-between;">
    <a href="../controlling-task-behavior" class="md-button">
        Previous <i class="fas fa-arrow-left"></i>
    </a>
    <a href="../recap" class="md-button">
        Next <i class="fas fa-arrow-right"></i>
    </a>
</div>
