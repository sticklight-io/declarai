# Azure OpenAI

To use Azure OpenAI models, you can set the following configuration options:

```py
import declarai

azure_model = declarai.azure_openai(
    azure_openai_key="<api-token>",
    azure_openai_api_base="<api-base>",
    deployment_name="<deployment-name>",
    api_version="<api-version>",
    headers={"<header-key>": "<header-value>"},
    timeout="<timeout>",
    request_timeout="<request_timeout>",
    stream="<stream>",
)
```

| Argument              | <div style="width:180px">Env Variable</div> | Required? |
|-----------------------|---------------------------------------------|:---------:|
| azure_openai_key      | `DECLARAI_AZURE_OPENAI_KEY`                 |     ✅     |
| azure_openai_api_base | `DECLARAI_AZURE_OPENAI_API_BASE`            |     ✅     |
| deployment_name       | `DECLARAI_AZURE_OPENAI_DEPLOYMENT_NAME`     |     ✅     |
| api_version           | `DECLARAI_AZURE_OPENAI_API_VERSION`         |           |
| headers               |                                             |           |
| timeout               |                                             |           |
| request_timeout       |                                             |           |
| stream                |                                             |           |

## Getting an API key, API base, and Deployment name

To obtain the above settings, you will need to create an account on
the [Azure OpenAI](https://azure.microsoft.com/en-us/services/cognitive-services/)
website. Once you have created an account, you will need to create a resource.

Please follow the instructions on
the [Azure OpenAI](https://learn.microsoft.com/en-us/azure/ai-services/openai/quickstart?tabs=command-line&pivots=programming-language-python)

## Setting the API key

You can set your API key at runtime like this:

```python
import declarai

my_azure_model = declarai.azure_openai(
    deployment_name="my-model",
    azure_openai_key="<your API key>",
    azure_openai_api_base="https://<my-azure-domain>.com",
)
```

However, it is preferable to pass sensitive settings as an environment variable: `DECLARAI_AZURE_OPENAI_API_KEY`.

To establish your Azure OpenAI API key as an environment variable, launch your terminal and execute the following
command,
substituting <your API key> with your actual key:

```shell
export DECLARAI_AZURE_OPENAI_KEY=<your API key>
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
import declarai

azure_model = declarai.azure_openai(
    deployment_name="my-model",
    azure_openai_key="<your API key>",
    azure_openai_api_base="https://<my-azure-domain>.com",
    headers="<my-headers>"
)


@azure_model.task(llm_params={"temperature": 0.5, "max_tokens": 1000})  # (1)!
def generate_song():
    """
    Generate a song about declarai
    """

```

1. Pass only the parameters you want to change. The rest will be set to their default values.
