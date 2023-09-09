import csv
import json
import requests
from flask import make_response
from bson import json_util
from bson.objectid import ObjectId
from response import make_json_response

from database import db
collection2 = db.chatbot_input

def get_all(collection):
    cursor = collection.find()
    return make_json_response(json_util.dumps(cursor), 200)


def get_by_id(id, collection):
    cursor = collection.find_one({"_id": ObjectId(id)})
    return make_json_response(json_util.dumps(cursor), 200)


def delete_all(collection):
    try:
        result = collection.delete_many({})
        deleted_count = result.deleted_count
        return make_json_response(f"Deleted {deleted_count} documents successfully", 200)
    except Exception as e:
        return make_json_response(str(e), 500)


def unsupported_method():
    return make_json_response("Request type not supported", 400)


def insert_and_get(rows, collection):    
    insertManyResult = collection.insert_many(rows)
    insertedRowsCursor = collection.find({"_id": {"$in": insertManyResult.inserted_ids}})
    
    return json_util.dumps(list(insertedRowsCursor))
