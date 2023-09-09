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

import requests
from bson import json_util
from response import make_json_response

import os
import json
import urllib3
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
import csv

collection = db.chatbot_input

def csv_to_json():
    csv_file_path = r'backend\anthropic\inputs\Applebead.28-02-2023 breakdown.csv'  # Replace with the path to your CSV file
    csv_data = []

    with open(csv_file_path, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            csv_data.append(row)

    csv_data_as_string = json.dumps(csv_data)
    return csv_data_as_string


def call_anthropic(question):
    prompt = f"\n\nHuman: {question}\n\nAssistant:"

    # Defaults
    ENDPOINT_URL = os.environ.get("ENDPOINT_URL", "https://api.anthropic.com/v1/complete")
    DEFAULT_MODEL = os.environ.get("DEFAULT_MODEL","claude-2")

    # set model params
    data = {
        "model": DEFAULT_MODEL,
        "temperature": 0,
        "max_tokens_to_sample": 128
    }

    data["prompt"] = prompt

    headers = {
        "anthropic-version": "2023-06-01", 
        "x-api-key": "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",
        "content-type": "application/json",
        "accept": "application/json"
    }
    http = urllib3.PoolManager()
    try:
        response = http.request(
            "POST",
            ENDPOINT_URL,
            body=json.dumps(data),
            headers=headers
        )
        if response.status != 200:
            raise Exception(f"Error: {response.status} - {response.data}")
        # print(response.data)
        generated_text = json.loads(response.data)["completion"].strip()
        print(generated_text)
        return generated_text
    except Exception as err:
        print(err)
        raise


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
