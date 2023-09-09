# TODO: if fail, paraphrase and retry query
# TODO: pay for premium to avoid rate limit for big queries
# TODO: .csvs need to be cleaned to reduce token count
# TODO: memory not implemented (cannot be implemented)

# Takes in csv as input.

from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType
from langchain.agents import create_csv_agent
import os
from dotenv import load_dotenv

def response_csv(query):
    load_dotenv()

    agent = create_csv_agent(
        ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613", openai_api_key = os.getenv("openai_api_key")
    ),
        ["backend\chatbot_response\inputs\instruments-cleaned.csv", "backend\chatbot_response\inputs\market-values-cleaned.csv"],
        verbose=False,
        agent_type=AgentType.OPENAI_FUNCTIONS,
    )

    # query: "can you determine the total marketValue of Private Equity?"
    # print(agent.run(query))

    response = agent({"input":query})
    print(response["output"])

query = "can you determine the total marketValue of Private Equity?" 
response_csv(query)