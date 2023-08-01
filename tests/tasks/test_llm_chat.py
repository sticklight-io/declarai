from unittest.mock import MagicMock
from pytest import fixture
from declarai.operators.openai_operators.message import Message
from declarai.tasks.llm_chat import LLMChat

CHAT_TEMPLATE = "{system_prompt}{output_instructions}"
TEMPLATE_KWARGS = {
    "system_prompt": "You are an assistant making people laugh.",
    "output_instructions": "",
}

SYSTEM_MESSAGE = Message(
    message="You are an assistant making people laugh.",
    role="system",
)


def test_chat_message():
    message = Message(
        message="Hello",
        role="user",
    )
    assert message.message == "Hello"
    assert message.role == "user"
    assert message.__repr__() == "user: Hello"
    assert message.__eq__(Message(message="Hello", role="user"))
    assert not message.__eq__(Message(message="Hello", role="assistant"))
    assert not message.__eq__(Message(message="Hallo", role="user"))


@fixture
def llm_chat():
    test_llm = MagicMock()
    test_llm.predict.return_value = MagicMock()
    llm_chat = LLMChat(
        template=CHAT_TEMPLATE,
        template_kwargs=TEMPLATE_KWARGS,
        llm=test_llm,
        prompt_kwargs={"structured": False},
    )
    return llm_chat


def test_llm_compile(llm_chat):
    user_message = Message(
        message="Hallo",
        role="user",
    )
    assert llm_chat.compile() == [SYSTEM_MESSAGE]
    assert llm_chat.compile(return_prompt=True) == f"{repr(SYSTEM_MESSAGE)}\n"
    assert llm_chat.compile(message=user_message.message) == [
        SYSTEM_MESSAGE,
        user_message,
    ]
    assert (
        llm_chat.compile(message="Hallo", return_prompt=True)
        == f"{repr(SYSTEM_MESSAGE)}\n{repr(user_message)}\n"
    )
    assert llm_chat.compile(message="Hallo", return_prompt=False) == [
        SYSTEM_MESSAGE,
        user_message,
    ]


def test_llm_compile_with_kwargs():
    test_llm = MagicMock()
    test_llm.predict.return_value = MagicMock()
    system_message = Message(
        message="You are a translator from english to {language}", role="system"
    )
    llm_chat = LLMChat(
        template=CHAT_TEMPLATE,
        template_kwargs={
            "system_prompt": system_message.message,
            "output_instructions": "",
        },
        llm=test_llm,
    )
    assert llm_chat.compile(language="french") == [
        Message(message="You are a translator from english to french", role="system")
    ]
    assert (
        llm_chat.compile(language="french", return_prompt=True)
        == f"{repr(Message(message='You are a translator from english to french', role='system'))}\n"
    )
    assert llm_chat.compile(language="french", return_prompt=False) == [
        Message(message="You are a translator from english to french", role="system")
    ]
    assert llm_chat.compile(language="french", message="Hello") == [
        Message(message="You are a translator from english to french", role="system"),
        Message(message="Hello", role="user"),
    ]


def test_llm_chat(llm_chat):
    llm_chat.llm.predict.return_value.response = "Helloululu"
    assistant_message = Message(
        message="Helloululu",
        role="assistant",
    )

    res = llm_chat.send("Hello")
    user_message = Message(
        message="Hello",
        role="user",
    )
    assert llm_chat.llm.predict.called
    assert res == "Helloululu"
    assert llm_chat.conversation == [user_message, assistant_message]
    assert llm_chat.system == repr(SYSTEM_MESSAGE)
    assert llm_chat._system_message == SYSTEM_MESSAGE
    assert llm_chat.llm_response.response == "Helloululu"
    assert llm_chat.compile() == [SYSTEM_MESSAGE, user_message, assistant_message]
    assert (
        llm_chat.compile(return_prompt=True)
        == f"{repr(SYSTEM_MESSAGE)}\n{repr(user_message)}\n{repr(assistant_message)}\n"
    )
    llm_chat.llm.predict.return_value.response = "Halloululu"
    second_user_message = Message(
        message="Hallo",
        role="user",
    )

    assert llm_chat.compile(message="Hallo") == [
        SYSTEM_MESSAGE,
        user_message,
        assistant_message,
        second_user_message,
    ]
    res = llm_chat.send("Hallo")
    assert res == "Halloululu"
    assert llm_chat.llm_response.response == "Halloululu"
    second_assistant_message = Message(
        message="Halloululu",
        role="assistant",
    )
    assert llm_chat.conversation == [
        user_message,
        assistant_message,
        second_user_message,
        second_assistant_message,
    ]


def test_llm_chat_system():
    test_llm = MagicMock()
    test_llm.predict.return_value = MagicMock()
    greeting_message = Message(
        message="Let me first introduce myself as the funniest chatbot in the world",
        role="assistant",
    )

    llm_chat = LLMChat(
        template=CHAT_TEMPLATE,
        template_kwargs=TEMPLATE_KWARGS,
        llm=test_llm,
        system=SYSTEM_MESSAGE.message,
        greeting="Let me first introduce myself as the funniest chatbot in the world",
    )

    assert llm_chat._system_message.message == SYSTEM_MESSAGE.message
    assert llm_chat.system == f"{repr(SYSTEM_MESSAGE)}"
    assert llm_chat._greeting_message == greeting_message
    assert llm_chat.greeting == repr(greeting_message)

    assert llm_chat.compile() == [SYSTEM_MESSAGE, greeting_message]


def test_llm_chat_system_with_kwargs():
    test_llm = MagicMock()
    test_llm.predict.return_value = MagicMock()
    system_message = Message(
        message="You are a translator from english to {language}", role="system"
    )
    llm_chat = LLMChat(
        template=CHAT_TEMPLATE,
        template_kwargs={
            "system_prompt": system_message.message,
            "output_instructions": "",
        },
        prompt_kwargs={"structured": False},
        llm=test_llm,
    )
    llm_chat.llm.predict.return_value.response = "Bonjur"
    assert llm_chat.send(language="french", message="Hello") == "Bonjur"
    assert llm_chat.last_compiled_messages == [
        Message(message="You are a translator from english to french", role="system"),
        Message(message="Hello", role="user"),
    ]
