import csv
import json
import requests
from flask import make_response
from bson import json_util
from bson.objectid import ObjectId
from response import make_json_response

from database import db

def get_all(collection):
    cursor = collection.find()
    return make_json_response(json_util.dumps(cursor), 200)


def get_by_id(id, collection):
    cursor = collection.find_one({"_id": ObjectId(id)})
    return make_json_response(json_util.dumps(cursor), 200)


def update_by_id(id, body, collection):
    cursor = collection.find_one({"_id": ObjectId(id)})
    query = {"_id": ObjectId(id)}
    update = {"$set": body}

    result = collection.find_one_and_update(query, update, return_document=pymongo.ReturnDocument.BEFORE)
    return make_json_response(json_util.dumps(cursor), 200)


def unsupported_method():
    return make_json_response("Request type not supported", 400)