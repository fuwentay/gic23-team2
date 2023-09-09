# TODO: if fail, paraphrase and retry query
# TODO: pay for premium to avoid rate limit for big queries
# TODO: .csvs need to be cleaned to reduce token count
# TODO: memory not implemented (cannot be implemented)

# Takes in csv as input.

from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType
from langchain.agents import create_csv_agent
from langchain.agents import create_pandas_dataframe_agent
import os
from dotenv import load_dotenv
import pandas as pd

def response_pd(query):
    load_dotenv()

    df1 = pd.read_csv("backend\chatbot_response\inputs\instruments-cleaned.csv")
    df2 = pd.read_csv("backend\chatbot_response\inputs\market-values-cleaned.csv")

    agent = create_pandas_dataframe_agent(
        ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613", openai_api_key = os.getenv("openai_api_key")
    ),
        [df1, df2],
        verbose=True,
        agent_type=AgentType.OPENAI_FUNCTIONS,
    )

    # query: "can you determine the total marketValue of Private Equity?"
    # print(agent.run(query))

    response = agent({"input":query})
    return response["output"]


query = "What is the total marketValue of Private Equity?" 
print(response_pd(query))