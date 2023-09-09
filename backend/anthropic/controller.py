from .services import *
from flask import Blueprint, request, jsonify

import traceback
import logging
from database import db

chatbot_blueprint = Blueprint("chatbot", __name__)
collection = db.chatbot


@chatbot_blueprint.route("/getAllMessages", methods=['GET', 'POST'])
def get_all_messages():
    if request.method == 'GET':
        messages = list(collection.find())
    for message in messages:
        message["_id"] = str(message["_id"])  # Convert ObjectID to string
        #answer = call_anthropic(question)
        question = message.get("text")
        if question:
            answer = call_anthropic(question)
            message["answer"] = answer
        else:
            message["answer"] = "No question field in the message"
    return jsonify(messages)

@chatbot_blueprint.route("/insertMessages", methods=['POST'])
def insert_messages():
    if request.method == 'POST':
        new_message = request.json
        result = collection.insert_one(new_message)
        new_message["_id"] = str(result.inserted_id)  # Convert ObjectID to string
        return jsonify(new_message), 201

@chatbot_blueprint.route("/clearAllMessages", methods=['POST'])
def clear_all_messages():
    result = collection.delete_many({})
    return jsonify({"message": f"All messages cleared, {result.deleted_count} documents deleted."})