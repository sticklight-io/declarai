To use OpenAI models, you can set the following configuration options:

| Setting | Env Variable     | Runtime Variable | Required? | Notes |
| --- |------------------| --- |  :---: | --- |
| API key | `OPENAI_API_KEY` | `settings.openai.api_key` | ✅ | |


## Getting an API key

To obtain an OpenAI API key, follow these steps:

1. [Log in](https://platform.openai.com/) to your OpenAI account (sign up if you don't have one)
2. Go to the "API Keys" [page](https://platform.openai.com/account/api-keys) under your account settings.
3. Click "Create new secret key." A new API key will be generated. Make sure to copy the key to your clipboard, as you will not be able to see it again.

## Setting the API key

You can set your API key at runtime like this:

```python
from declarai import Declarai

declarai = Declarai(provide="openai", model="gpt4", openai_token="<your API key>")
```

However, it is preferable to pass sensitive settings as an environment variable: `DECLARAI_OPENAI_API_KEY`. 

To establish your OpenAI API key as an environment variable, launch your terminal and execute the following command, substituting <your API key> with your actual key:

```shell
export DECLARAI_OPENAI_API_KEY=<your API key>
```

This action will maintain the key for the duration of your terminal session. To ensure a longer retention, modify your terminal's settings or corresponding environment files.
