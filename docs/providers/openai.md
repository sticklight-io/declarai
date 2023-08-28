To use OpenAI models, you can set the following configuration options:

```py
import declarai

azure = declarai.openai(
    openai_token="<api-token>",
    model="<model>",
    headers={"<header-key>": "<header-value>"},
    timeout="<timeout>",
    request_timeout="<request_timeout>",
    stream="<stream>", )
```


| Setting         | <div style="width:180px">Env Variable</div> | <div style="width:280px">Runtime Variable</div>   | Required? |
|-----------------|---------------------------------------------|---------------------------------------------------|:---------:|
| API key         | `DECLARAI_OPENAI_API_KEY`                   | `Declarai(... openai_token=<api-token>)`          |     ✅     |
| Headers         |                                             | `Declarai(... headers=<headers>)`                 |           |
| Timeout         |                                             | `Declarai(... timeout=<timeout>)`                 |           |
| Request timeout |                                             | `Declarai(... request_timeout=<request_timeout>)` |           |
| Stream          |                                             | `Declarai(... stream=<stream>)`                   |           |

## Getting an API key

To obtain an OpenAI API key, follow these steps:

1. [Log in](https://platform.openai.com/) to your OpenAI account (sign up if you don't have one)
2. Go to the "API Keys" [page](https://platform.openai.com/account/api-keys) under your account settings.
3. Click "Create new secret key." A new API key will be generated. Make sure to copy the key to your clipboard, as you
   will not be able to see it again.

## Setting the API key

You can set your API key at runtime like this:

```python
from declarai import Declarai

declarai = Declarai(provide="openai", model="gpt4", openai_token="<your API key>")
```

However, it is preferable to pass sensitive settings as an environment variable: `DECLARAI_OPENAI_API_KEY`.

To establish your OpenAI API key as an environment variable, launch your terminal and execute the following command,
substituting <your API key> with your actual key:

```shell
export DECLARAI_OPENAI_API_KEY=<your API key>
```

This action will maintain the key for the duration of your terminal session. To ensure a longer retention, modify your
terminal's settings or corresponding environment files.

## Control LLM Parameters

OpenAI models have a number of parameters that can be tuned to control the output of the model. These parameters are
passed to the declarai task/chat interface as a dictionary. The following parameters are supported:

| Parameter           | Type    | Description                                                                                                                                                             | Default |
|---------------------|---------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------|
| `temperature`       | `float` | Controls the randomness of the model. Lower values make the model more deterministic and repetitive. Higher values make the model more random and creative.             | `0`     |
| `max_tokens`        | `int`   | Controls the length of the output.                                                                                                                                      | `3000`  |
| `top_p`             | `float` | Controls the diversity of the model. Lower values make the model more repetitive and conservative. Higher values make the model more random and creative.               | `1`     |
| `frequency_penalty` | `float` | Controls how often the model repeats itself. Lower values make the model more repetitive and conservative. Higher values make the model more random and creative.       | `0`     |
| `presence_penalty`  | `float` | Controls how often the model generates new topics. Lower values make the model more repetitive and conservative. Higher values make the model more random and creative. | `0`     |

Pass your custom parameters to the declarai task/chat interface as a dictionary:

```python
from declarai import Declarai

declarai = Declarai(provide="openai", model="gpt4", openai_token="<your API key>")


@declarai.task(llm_params={"temperature": 0.5, "max_tokens": 1000})  # (1)!
def generate_song():
    """
    Generate a song about declarai
    """

```

1. Pass only the parameters you want to change. The rest will be set to their default values.
