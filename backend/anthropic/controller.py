from .services import *
from flask import Blueprint, request, jsonify

import traceback
import logging
from database import db
from pymongo import DESCENDING
from threading import Thread

chatbot_blueprint = Blueprint("chatbot", __name__)
collection = db.chatbot


@chatbot_blueprint.route("/getAllMessages", methods=['GET'])
def get_all_messages():
    if request.method == 'GET':
        # Fetch all messages from the database
        messages = list(collection.find())

        # Convert ObjectID to string and prepare the response
        for message in messages:
            message["_id"] = str(message["_id"])
            message["sender"] = "user"  # Add a sender field to each message
            if "answer" in message:
                message["answer"] = {"text": message["answer"], "sender": "bot"}  # Wrap the answer in an object with a sender field
        
        return jsonify(messages)
    else:
        return jsonify({"error": "Method not allowed"}), 405
# @chatbot_blueprint.route("/insertMessages", methods=['POST'])
# def insert_messages():
#     if request.method == 'POST':
#         new_message = request.json
#         result = collection.insert_one(new_message)
#         new_message["_id"] = str(result.inserted_id)  # Convert ObjectID to string
#         return jsonify(new_message), 201

@chatbot_blueprint.route("/insertMessages", methods=['POST'])
def send_message():
    # Get the message from the request
    data = request.get_json()
    message_text = data.get("text")
    
    # Create a new message document in the database
    message_doc = {"text": message_text}
    result = collection.insert_one(message_doc)
    
    # Start a background task to generate an answer
    thread = Thread(target=generate_answer, args=(result.inserted_id, message_text))
    thread.start()
    
    # Return the message ID to the client
    return jsonify({"message_id": str(result.inserted_id)})

def generate_answer(message_id, message_text):
    # Generate an answer using the call_anthropic function
    answer = call_anthropic(message_text)
    
    # Update the message document in the database with the answer
    collection.update_one({'_id': message_id}, {'$set': {'answer': answer}})

@chatbot_blueprint.route("/clearAllMessages", methods=['POST'])
def clear_all_messages():
    result = collection.delete_many({})
    return jsonify({"message": f"All messages cleared, {result.deleted_count} documents deleted."})

# @chatbot_blueprint.route("/getResponse", methods=['GET'])
# def get_response():
#     if request.method == 'GET':
#         latest_message = collection.find().sort([('_id', DESCENDING)]).limit(1)[0]
#         latest_message["_id"] = str(latest_message["_id"])  # Convert ObjectID to string

#         question = latest_message.get("text")
#         if question:
#             answer = call_anthropic(question)
#             latest_message["answer"] = answer
#         else:
#             latest_message["answer"] = "No question field in the message"
        
#         return jsonify(latest_message)