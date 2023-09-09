# FIXME: memory cannot be implemented for pandas dataframe agent. this is not a working file
# Takes in df as input. This way of invoking displays the thought and action of the agent.

from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType
from langchain.agents import create_pandas_dataframe_agent
from langchain.memory import ConversationBufferWindowMemory, ConversationSummaryMemory, ConversationKGMemory, CombinedMemory

import os
from dotenv import load_dotenv

import pandas as pd

load_dotenv()

llm_code = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo", openai_api_key = os.getenv("openai_api_key")) #gpt-3.5-turbo-16k-0613
llm_context = ChatOpenAI(temperature=0.5, model_name="gpt-3.5-turbo", openai_api_key = os.getenv("openai_api_key")) #gpt-3.5-turbo

chat_history_buffer = ConversationBufferWindowMemory(
    k=5,
    memory_key="chat_history_buffer",
    input_key="input"
    )

chat_history_summary = ConversationSummaryMemory(
    llm=llm_context, 
    memory_key="chat_history_summary",
    input_key="input"
    )

chat_history_KG = ConversationKGMemory(
    llm=llm_context, 
    memory_key="chat_history_KG",
    input_key="input",
    )

memory = CombinedMemory(memories=[chat_history_buffer, chat_history_summary, chat_history_KG])

# df1 = pd.read_csv("inputs\instruments-cleaned.csv")
# df2 = pd.read_csv("inputs\market-values-cleaned.csv")

df1 = pd.read_csv("dummy_input\sample1.csv")
df2 = pd.read_csv("dummy_input\sample2.csv")

pd_agent = create_pandas_dataframe_agent(
    llm_code, 
    df1, 
    verbose=True, 
    memory=memory,
    input_variables=['df_head', 'input', 'agent_scratchpad', 'chat_history_buffer', 'chat_history_summary', 'chat_history_KG']
    )

pd_agent.run("what is the instrument ID of ETFs?")