from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType
from langchain.agents import create_csv_agent
from langchain.agents import create_pandas_dataframe_agent
import os
from dotenv import load_dotenv
import pandas as pd

from pymongo import MongoClient

# TODO: move to env file
mongopass = "mongodb+srv://root:gichackathon2023@gichackathon2023.xxk3lqm.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(mongopass)
db = client.GICHackathon2023

collection = db.ingest

data=collection.find()
df=pd.DataFrame(data)
print(df)

df1 = pd.read_csv("backend/chatbot_response/inputs/instruments-cleaned.csv")
df2 = pd.read_csv("backend/chatbot_response/inputs/market-values-cleaned.csv")

agent = create_pandas_dataframe_agent(
    ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613", openai_api_key="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"
               ),
    [df1, df2],
    verbose=False,
    agent_type=AgentType.OPENAI_FUNCTIONS,
)

query="what is the total marketValue of Private Equity?"
response = agent({"input": query})
print(response["output"])