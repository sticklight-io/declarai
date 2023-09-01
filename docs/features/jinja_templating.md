## Jinja Templating

[Jinja](https://jinja.palletsprojects.com/en/2.11.x/) is a templating language for Python.

We can use Jinja to create templates for our tasks. This is useful when:
- Task has a lot of boilerplate code
- Task has a lot of parameters.
- You want to control the task's prompt structure.

For example, let's say we want to create a task that takes in a string and ranks its sentiment. We
can use Jinja to create a template for this task:

```python
import declarai
from typing import List

gpt_35 = declarai.openai(model="gpt-3.5-turbo")


@gpt_35.task
def sentiment_classification(string: str, examples: List[str, int]) -> int:
    """
    Classify the sentiment of the provided string, based on the provided examples.
    The sentiment is ranked on a scale of 1-5, with 5 being the most positive.
    {% for example in examples %}
    {{ example[0] }} // {{ example[1] }}
    {% endfor %}
    {{ string }} //
    """


sentiment_classification.compile(string="I love this product but there are some annoying bugs",
                         examples=[["I love this product", 5], ["I hate this product", 1]])

>>> {'messages': [
    system: respond only with the value of type int:, # (1)!
    user: Classify the sentiment of the provided string, based on the provided examples. The sentiment is ranked on a scale of 1-5, with 5 being the most positive. # (2)!
          I love this product // 5
          I hate this product // 1
          I love this product //
    ]
}

sentiment_classification(string="I love this product but there are some annoying bugs",
                         examples=[["I love this product", 5], ["I hate this product", 1]])

>>> 4
```


1. The system message is generated based on the return type `int` of the function.
2. The user message is generated based on the docstring of the function. The Jinja template is rendered with the provided parameters.


