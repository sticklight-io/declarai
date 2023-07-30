# Debugging tasks

So it all seems pretty magical up to this point, but what if you want to see what's going on behind the scenes?
Being able to debug your tasks is a very important part of the development process, and **Declarai** makes it easy for you.

## Compiling tasks
The first and simplest tool to better understand what's happening under the hood is the `compile` method.

Let's take the last example from the previous section and add a call to the `compile` method:
```python
@declarai.task
def movie_recommender(user_input: str) -> Dict[str, str]:
    """
    Recommend a selection of movies to watch based on the user input
    For each movie provide a short description as well
    :param user_input: The user's input
    :return: A dictionary of movie names and descriptions
    """
```
```python
print(movie_recommender.compile())
> 
Recommend a selection of movies to watch based on the user input 
For each movie provide a short description as well # (1)! 
Inputs: # (2)!
user_input: {user_input} # The user's input 

# (3)!
The output should be a markdown code snippet formatted in the following schema, including the leading and trailing '```json' and '```': 
 ```json
    {{
        "declarai_result": Dict[str, str]  # A dictionary of movie names and descriptions
    }}
 .```
```

1. Here we can see our original task definition taken from the docstring.
2. Our task's inputs is transformed into a placeholder for the actual value accompanied by the value's name and meaning.
3. The expected output is also transformed into a placeholder for the actual value accompanied by the value's type and meaning.

What we're seeing here is the template for this specific task. It is built so that when called at runtime, 
it will be populated with the real values passed to our task.

!!! warning

     As you can see, that the actual prompt being sent to the model is a bit different than the original docstring.
     Even though Declarai incorporates best practices for prompt engineering while maintaining as little interference as possible with user prompts, 
     it is still possible that the model will not generate the desired output. For this reason it is important to be able to debug your tasks and understand what actually got sent to the model

## Compiling tasks with real values
The `compile` method can also be used to view the prompt with the real values of the parameters.
This is useful when prompts might behave differently for different inputs.

```python
print(movie_recommender.compile(user_input="I want to watch a movie about space"))
> 
Recommend a selection of movies to watch based on the user input 
For each movie provide a short description as well 
Inputs: # (1)! 
user_input: I want to watch a movie about space # The user's input 

The output should be a markdown code snippet formatted in the following schema, including the leading and trailing '```json' and '```': 
 ```json
    {{
        "declarai_result": Dict[str, str]  # A dictionary of movie names and descriptions
    }}
 .```
```

1. The actual value of the parameter is now populated in the placeholder and we have our final prompt!


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
