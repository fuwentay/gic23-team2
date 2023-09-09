from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType
from langchain.agents import create_csv_agent
from langchain.agents import create_pandas_dataframe_agent
import os
from dotenv import load_dotenv
import pandas as pd
from response import make_json_response
from bson import json_util

from database import db
import json

collection = db.chatbot_input

import requests
from bson import json_util
from response import make_json_response

def response_pd(query):
    load_dotenv()

    agent = create_pandas_dataframe_agent(
        ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613", openai_api_key = os.getenv("openai_api_key")
    ),
        retrieve_pd(),
        # [df1, df2],
        verbose=False,
        agent_type=AgentType.OPENAI_FUNCTIONS,
    )

    response = agent({"input":query})
    return response["output"]

def retrieve_pd():
    distinct_filenames = collection.distinct("filename")
    dfs = []
    fields_to_exclude = {"_id": 0, "filename": 0}
    for filename in distinct_filenames:
        data = list(collection.find({"filename": filename}, projection=fields_to_exclude))
        df = pd.DataFrame(data)
        dfs.append(df)
    return dfs

# def convert_json_to_pd():
#     # save as JSON
#     data_from_mongodb = list(collection.find())
#     if data_from_mongodb:
#     # Extract the JSON content from the MongoDB document
#         json_data = data_from_mongodb["content"]

#         # Convert the JSON content to a Python dictionary or list
#         # This step depends on how the data is structured in your JSON
#         # For example, if the JSON data is stored as a JSON string:
#         data_dict = json.loads(json_data)

#         # Create a Pandas DataFrame
#         df = pd.DataFrame(data_dict)
#         return df
#     else:
#         print("JSON data not found in MongoDB.")

# def response_csv(query):
#     load_dotenv()

#     agent = create_csv_agent(
#         ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613", openai_api_key = os.getenv("openai_api_key")
#     ),
#         ["backend\chatbot_response\inputs\instruments-cleaned.csv", "backend\chatbot_response\inputs\market-values-cleaned.csv"],
#         verbose=False,
#         agent_type=AgentType.OPENAI_FUNCTIONS,
#     )

#     # query: "can you determine the total marketValue of Private Equity?"
#     # print(agent.run(query))

#     response = agent({"input":query})
#     return response["output"]
