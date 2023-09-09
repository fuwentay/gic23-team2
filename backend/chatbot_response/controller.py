from .services import *
from flask import Blueprint, request, jsonify

import traceback
import logging
from database import db

chatbot_blueprint = Blueprint("chatbot", __name__)
collection = db.chatbot

@chatbot_blueprint.route("/chat")
def getResponse():
    # query = "can you determine the total marketValue of Private Equity?"
    try:
        json_data = csv_to_json()
        query = "\n What are the different financial types?"
        question = "Here is the csv data: " + json_data + query
        return call_anthropic(question)
    # TODO: paraphrase using openai api until valid response.
    except Exception as e:
        logging.error(traceback.format_exc())
        # Logs the error appropriately.
        return "Sorry, could you please repeat what you said? You could try paraphrasing what you said."


# @chatbot_blueprint.route("/chat")
# def getResponse():
#     # query = "can you determine the total marketValue of Private Equity?"
#     try:
#         return response_pd("on 31/1/2020 12:00:00am, can you determine the total marketValue of Private Equity?")
#     # TODO: paraphrase using openai api until valid response.
#     except Exception as e:
#         logging.error(traceback.format_exc())
#         # Logs the error appropriately.
#         return "Sorry, could you please repeat what you said? You could try paraphrasing what you said."


@chatbot_blueprint.route("/getAllMessages", methods=['GET', 'POST'])
def get_all_messages():
    if request.method == 'GET':
        messages = list(collection.find())
    for message in messages:
        message["_id"] = str(message["_id"])  # Convert ObjectID to string
    return jsonify(messages)


@chatbot_blueprint.route("/insertMessages", methods=['POST'])
def insert_messages():
    if request.method == 'POST':
        new_message = request.json
        result = collection.insert_one(new_message)
        new_message["_id"] = str(result.inserted_id)  # Convert ObjectID to string
        return jsonify(new_message), 201


# import csv
# from flask import Flask, request, render_template, Response
# from pymongo import MongoClient
# import json
# import io

# @chatbot_blueprint.route('/exportToCSV', methods=['GET'])
# def export_to_csv():
#     # Retrieve data from MongoDB as JSON
#     data_from_mongodb = list(collection.find())
    
#     # Check if there is data to export
#     if not data_from_mongodb:
#         return "No data to export."

#     # Convert JSON data to a list of dictionaries
#     data_list = [json.loads(json.dumps(doc, default=str)) for doc in data_from_mongodb]

#     # Define the CSV file's column headers (use the keys of the first dictionary)
#     headers = data_list[0].keys()

#     # Create a CSV response
#     def generate_csv():
#         csv_output = io.StringIO()
#         csv_writer = csv.DictWriter(csv_output, fieldnames=headers)
#         csv_writer.writeheader()
#         for data_row in data_list:
#             csv_writer.writerow(data_row)
#             csv_output.seek(0)
#             yield csv_output.getvalue()
#             csv_output.seek(0)
#             csv_output.truncate()

#     response = Response(generate_csv(), mimetype='text/csv')
#     response.headers["Content-Disposition"] = "attachment; filename=data.csv"

#     return response
