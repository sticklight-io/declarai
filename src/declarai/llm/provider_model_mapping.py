from typing import Literal, Union

# Based on documentation from https://platform.openai.com/docs/models/overview
ProviderOpenai = Literal["openai"]
ModelsOpenai = Literal[
    "gpt-4",
    "gpt-3.5-turbo",
    "text-davinci-003",
    "text-davinci-002",
    "code-davinci-002",
]


# Based on documentation from https://docs.cohere.com/reference/generate
ProviderCohere = Literal["Cohere"]
ModelsCohere = Literal[
    "command", "command-nightly", "command-light", "command-light-nightly"
]


ProviderAI21labs = Literal["AI21Labs"]
ModelsAI21labs = Literal["curie", "babbage"]

# Based on documentation from https://cloud.google.com/vertex-ai/docs/generative-ai/learn/models
ProviderGoogle = Literal["google"]
ModelsGoogle = Literal[
    "text-bison",
    "textembedding-gecko",
    "chat-bison",
    "code-bison",
    "codechat-bison",
    "code-gecko",
]

AllModels = Union[ModelsOpenai, ModelsCohere, ModelsAI21labs, ModelsGoogle]
