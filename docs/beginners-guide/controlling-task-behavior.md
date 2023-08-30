---
hide:
  - footer
---

# Controlling task behavior :control_knobs:

Task behavior can be controlled by any of the available interfaces in Python.
Controlling these parameters is key to achieving the desired results from the model.

### Passing parameters to the task :label:

In the following example, we'll create a task that suggests movies to watch based on a given input.

```python
import declarai

gpt_35 = declarai.openai(model="gpt-3.5-turbo")


@gpt_35.task
def movie_recommender(user_input: str):  # (1)!
    """
    Recommend a movie to watch based on the user input
    :param user_input: The user's input
    """  # (2)!
```

1. Notice how providing a type hint for the `user_input` parameter allows declarai to understand the expected input
   type.
2. Adding the param to the docstring allows declarai to communicate the **meaning** of this parameter to the model.

```python
print(movie_recommender(user_input="I want to watch a movie about space"))
> 'Interstellar'
```

### Using return types to control the output :gear:

This is a good start,
but let's say we want to have a selection of movies instead of a single suggestion.

```python
from typing import List
import declarai

gpt_35 = declarai.openai(model="gpt-3.5-turbo")


@gpt_35.task
def movie_recommender(user_input: str) -> List[str]:  # (1)!
    """
    Recommend a selection of movies to watch based on the user input
    :param user_input: The user's input
    :return: A list of movie recommendations
    """  # (2)!
```

1. Adding a return type hint allows declarai to parse the output of the llm into the provided type,
   in our case a list of strings.
2. Explaining the return value aids the model in returning the expected output and avoiding hallucinations.

```python
print(movie_recommender(user_input="I want to watch a movie about space"))
> ['Interstellar', 'Gravity', 'The Martian', 'Apollo 13', '2001: A Space Odyssey', 'Moon', 'Sunshine', 'Contact',
   'The Right Stuff', 'Hidden Figures']
```

!!! info

    Notice How the text in our documentation has changed from singular to plural form. 
    Maintaining consistency between the task's description and the return type is important for the model to understand the expected output.<br>
    For more best-practices, see [here](../../best-practices). 

Awesome!

Now we have a list of movies to choose from!

But what if we want to go even further :thinking:? <br>
Let's say we want the model to also provide a short description of each movie.

```python
from typing import Dict
import declarai

gpt_35 = declarai.openai(model="gpt-3.5-turbo")


@gpt_35.task
def movie_recommender(user_input: str) -> Dict[str, str]:  # (1)!
    """
    Recommend a selection of movies to watch based on the user input
    For each movie provide a short description as well
    :param user_input: The user's input
    :return: A dictionary of movie names and descriptions
    """  # (2)!
```

1. We've updated the return value to allow for the creation of a dictionary of movie names and descriptions.
2. We re-enforce the description of the return value to ensure the model understands the expected output.

```python
print(movie_recommender(user_input="I want to watch a movie about space"))
> {
    'Interstellar': "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.",
    'Gravity': 'Two astronauts work together to survive after an accident leaves them stranded in space.',
    'The Martian': 'An astronaut is left behind on Mars after his team assumes he is dead and must find a way to survive and signal for rescue.',
    'Apollo 13': 'The true story of the Apollo 13 mission, where an explosion in space jeopardizes the lives of the crew and their safe return to Earth.',
    '2001: A Space Odyssey': "A journey through human evolution and the discovery of a mysterious black monolith that may hold the key to humanity's future."
}
```

!!! info

    A good practice for code readability as well as great performing models is to use type hints and context in the docstrings.
    The better you describe the task, `:params` and `:return` sections within the docstring, the better the results will be.

!!! tip

    Try experimenting with various descriptions and see how far you can push the model's understanding!
    who knows what you'll find :open_mouth:!

<div style="display: flex; justify-content: space-between;">
    <a href="../simple-task" class="md-button">
        Previous <i class="fas fa-arrow-left"></i>
    </a>
    <a href="../debugging-tasks" class="md-button">
        Next <i class="fas fa-arrow-right"></i>
    </a>
</div>
