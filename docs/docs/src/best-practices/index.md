# Best practices

Prompt engineering is no simple task and there are various things to consider when creating a prompt.
In this page we provide our view and understanding of the best practices for prompt engineering.
These will help you create reliably performing tasks and chatbots that won't surprise you when deploying in production.

!!! warning

     While this guide will should help in creating reliable prompts for most cases, it is still possible that the model will not generate the desired output.
     For this reason we strongly recommend you test your tasks and bots on various inputs before deploying to production.<br>
     You can acheive this by writing integration tests or using our provided `evals` library to discover which models and wich
     versions perform best for your specific use case.


### Explicit is better than implicit

When creating a prompt, it is important to be as explicit as possible.
Declarai provide various interfaces to provide context and guidance to the model.

Reviewing the movie recommender example from the beginner's guide, we can see a collection of techniques to provide context to the model:
```python
@declarai.task
def movie_recommender(user_input: str) -> Dict[str, str]:
    """
    Recommend a selection of movies to watch based on the user input
    For each movie provide a short description as well
    :param user_input: The user's input
    :return: A dictionary of movie names and descriptions
    """ # (2)!
```

**Using type annotations** in the input and output create predictability in software and enforce a strict interface with the model.<br>
The types are read and enforced by Declarai at runtime so that a produced result of the wrong type will raise an error instead of
returned and causing unexpected behavior down the line.

**Docstrings** are used to provide context to the model and to the user.

 - **Task description** - The first part of the docstring is the task itself, make sure to address the expected inputs and how to use them
    You can implement various popular techniques into the prompt such as `few-shot`, which means providing example inputs and outputs for the model to learn from.

 - **Param descriptions** - Explaining the meaning of the input parameters helps the model better perform with the provided inputs.
    For example. when passing an argument called `input`, if you know that the expected input will be an email, or user message, it is best to explain this to the model.

 - **Return description** - While typing are a great base layer for declaring the expected output, 
    explaining the exact structure and logic behind this structure will help the model better perform.
    For example, given a return type of `Dict[str, str]`, explaining that this object will contain a mapping of movie names to their respective description 
    will help to model properly populate the resulting object.

### Language consistency and ambiguity

When providing prompts to the model, it is best practice to use language that correlates with the expected input and output.
For example, in the following, the prompt is written in single form, while the resulting output is in plural form. (i.e. a list)
```python
@declarai.task
def movie_recommender(user_input: str) -> List[str]:
    """
    Recommend a movie to watch based on the user input
    :param user_input: The user's input
    :return: Recommended movie
    """
```
This may easily confuse the model and cause it to produce unexpected results which will fail when parsing the results.
Instead, we could write the prompt as follows:
```python
@declarai.task
def movie_recommender(user_input: str) -> List[str]:
    """
    Recommend a selection of movies to watch based on the user input
    :param user_input: The user's input
    :return: A list of recommended movies
    """
```
This way it is clear to the model that we are expecting a list of movies and not a single movie.


### Falling back to string

In some cases, you might be working on a task or chat that has a mixture of behaviors that may not be consistent.
For example in this implementation of a calculator bot, the bot usually returns numbers, but for the scenario that an error occurs, it returns a string.
```python
@declarai.experimental.chat
class CalculatorBot:
    """
    You a calculator bot,
    given a request, you will return the result of the calculation
    If you have a problem with the provided input, you should return an error explaining the problem.
    For example, for the input: "1 + a" where 'a' is unknown to you, you should return: "Unknown symbol 'a'"
    """
    def send(self, message: str) -> Union[str, int]:
        ...
```
When using the created bot it should look like this:
```python
calc_bot = CalculatorBot()
print(calc_bot.send(message="1 + 3"))
#> 4
print(calc_bot.send(message="34 * b"))
#> Unknown symbol 'b'
```
This way, instead of raising an error, the bot returns a string that explains the problem and allows the user to recover from the 'broken' state.
