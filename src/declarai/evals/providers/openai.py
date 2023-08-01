from declarai import Declarai

openai_models = {
    # "open_openai_gpt_3_5_latest": Declarai(provider="openai", model="gpt-3.5-turbo"),
    "open_openai_gpt_3_5_0301": Declarai(
        provider="openai", model="gpt-3.5-turbo", version="0301"
    ),
    "open_openai_gpt_3_5_0613": Declarai(
        provider="openai", model="gpt-3.5-turbo", version="0613"
    ),
    # "open_openai_gpt_4_latest": Declarai(provider="openai", model="gpt-4"),
    "open_openai_gpt_4_0603": Declarai(
        provider="openai", model="gpt-4", version="0613"
    ),
}
