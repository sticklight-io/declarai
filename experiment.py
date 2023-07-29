import datetime
from typing import Dict, Callable

from wandb_addons.prompts import Trace

from declarai import Declarai, Sequence
from declarai.tasks.llm_task import LLMTaskType

declarai = Declarai(provider="openai", model="gpt-3.5-turbo", version="0301")


@declarai.task
def data_manipulation(data: Dict[str, str]) -> Dict[str, str]:
    """
    create a redacted version of the input data.
    any potentially private data in the input
    should be replaced with the first 2 characters of the original content
    followed by * for the entire of the remaining characters
    for example, "guy.b@company.com" should be redacted to "gu**************"
    Don't write any python code, only return the resulting json
    :param data: The data to anonymize
    :return: The anonymized data
    """
    return declarai.magic("redacted_info", data=data)


def redact_content(task: LLMTaskType) -> Callable:
    def redact(text: str):
        sequence = Sequence(
            data_manipulation.plan(data=task.plan(text=text)),
            reduce_strategy="CoT",
        )
        return sequence()['redacted_info']

    return redact


def log_before(task: LLMTaskType) -> Callable:
    task._start_time_ms = datetime.datetime.now().timestamp() * 1000


def log_after(task: LLMTaskType) -> Callable:
    status = "success"
    status_message = None,
    # response_text = response["choices"][0]["message"]["content"]
    response_text = task._result
    # token_usage = response["usage"].to_dict()
    token_usage = 100
    end_time_ms = round(datetime.datetime.now().timestamp() * 1000)  # logged in milliseconds
    root_span = Trace(
        name="root_span",
        kind="llm",  # kind can be "llm", "chain", "agent" or "tool"
        status_code=status,
        status_message=status_message,
        metadata={"temperature": task._prompt_config.temperature,
                  "token_usage": token_usage,
                  "model_name": task._llm.model},
        start_time_ms=task._start_time_ms,
        end_time_ms=end_time_ms,
        inputs={"query": "Something"},
        outputs={"response": response_text},
    )

    # log the span to wandb
    root_span.log(name="openai_trace")


@declarai.task(
    before_hooks=[log_before],
    after_hooks=[log_after],
)
def extract_info(text: str) -> Dict[str, str]:
    """
    Extract the phone number, name and email from the provided text
    :param text: content to extract the info from
    :return: The info extracted from the text
    """
    return Declarai.magic(text=text)


res = extract_info(text="Hey jenny,"
                        "you can call me at 124-3435-132."
                        "You can also email me at georgia@coolmail.com"
                        "Have a great week!")
# print(res)
# {
#     'phone_number': '12*********',
#     'name': 'je****',
#     'email': 'ge**************'
# }

#
# import wandb
#
# # start a new wandb run to track this script
# wandb.init(
#     # set the wandb project where this run will be logged
#     project="llm-prompt-tracking",
#
#     # track hyperparameters and run metadata
#     config={
#         "learning_rate": 0.02,
#         "architecture": "CNN",
#         "dataset": "CIFAR-100",
#         "epochs": 10,
#     }
# )


    # except Exception as e:
    #     end_time_ms = round(datetime.datetime.now().timestamp() * 1000)  # logged in milliseconds
    #     status = "error"
    #     status_message = str(e)
    #     response_text = ""
    #     token_usage = {}
