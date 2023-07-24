# Introducing pragmatic llm
Using AI in your code shouldn't be difficult. Under the mission of bringing AI to the masses,
This repo is meant to abstract the know-how of AI and make it accessible to everyone.

If you know how to write python code and have written any doc-string in your life, you are ready to use this library!

## Installation
```bash
pip install pragmatic-llm
```

## Setup
```bash
export USE_AI_OPENAAI_TOKEN=<your openai token>
```

## Usage:
```python
from typing import List
from use_ai import use_ai, magic


@use_ai
def extract_names(text: str) -> List[str]:
    """
    Extracts names from text
    :param text: text to extract names from
    :return: list of names
    """
    return magic(text)

print(extract_names(text="Hello, my name is John Doe. What's yours?"))
>>> ['John Doe']
```
That's it! You've written your first AI code!

pragmatic llm aims to promote clean and readable code by enforcing the use of doc-strings and typing.
The resulting code is readable and easily maintainable.

## Debugging
If you want to see what's going on under the hood, you can compile your code before execution:
```python
from use_ai import compile

compile(extract_names)

>>> 
compiled -> 
"""
Given the following inpput:
test: str  #  text to extract names from

apply the `extract_names` method to the input
The resulting values should be in the following format:
result: List[str]  #  list of names
{text}

```json
"""
```

## Plugins
pragmatic llm is built to be extensible. You can add from the provided plugins or implement your own.
```python
from typing import List
from use_ai import use_ai, magic, PromptLogger, ChatMemory, PromptCache, AICongig


ai_config = AICongig(
    provider='openai',
    model='gpt-3.5-turbo',
    determinism=0.5,
)


@use_ai(
    ai_config=ai_config,
    loggingProvide=PromptLogger,
    memory=ChatMemory,
    cache=PromptCache
)
def extract_names(text: str) -> List[str]:
    """
    Extracts names from text
    :param text: text to extract names from
    :return: list of names
    """
    return magic(text)
```


## Contributing
...