import anthropic

from langchain.chat_models import ChatAnthropic
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import AIMessage, HumanMessage, SystemMessage


chat = ChatAnthropic()

messages = [
    HumanMessage(
        content="Translate this sentence from English to French. I love programming."
    )
]
response = chat(messages)

print(response)