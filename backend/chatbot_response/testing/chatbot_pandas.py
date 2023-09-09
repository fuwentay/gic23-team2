# Takes in df as input. This way of invoking displays the thought and action of the agent.

from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType
from langchain.agents import create_pandas_dataframe_agent

import os
from dotenv import load_dotenv

import pandas as pd

load_dotenv()

df1 = pd.read_csv("backend\chatbot_response\inputs\instruments-cleaned.csv")
df2 = pd.read_csv("backend\chatbot_response\inputs\market-values-cleaned.csv")

agent = create_pandas_dataframe_agent(
    OpenAI(temperature=0, openai_api_key = os.getenv("openai_api_key")), 
    [df1, df2], 
    verbose=True,
    return_intermediate_steps=False
)

agent.run("can you determine the total marketValue of Private Equity?")