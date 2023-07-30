## Plan task :material-airplane-clock:
Once you have defined your task, you can create a plan for it that is already populated with the real values of the parameters.

The plan is an object you call and get the results. This is very helpful when you want to populate the task with the real values of the parameters but delay the execution of it. 
    
```py

from declarai import init_declarai, magic

task = init_declarai(provider="openai", model="gpt-3.5-turbo")

@task
def say_something_about_movie(movie: str) -> str:  
    """
    Say something short about the following movie
    :param movie: The movie name
    """

    return magic(movie)

plan = say_something_about_movie.plan(movie="Avengers")

print(plan)
> #<declarai.tasks.base_llm_task.LLMTaskFuture object at 0x106795790>


# Execute the task by calling the plan
plan()
> ['I liked the action-packed storyline and the epic battle scenes.',
   "I didn't like the lack of character development for some of the Avengers."]
```


!!! warning "Important"
    The plan is an object you call and get the results. This is very helpful when you want to populate the task with the real values of the parameters but delay the execution of it.
    If you just want to execute the task, you can call the task directly.

    ```py
    res = say_something_about_movie(movie="Avengers")

    > ['I liked the action-packed storyline and the epic battle scenes.',
    "I didn't like the lack of character development for some of the Avengers."]
    ```