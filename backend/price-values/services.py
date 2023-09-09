import csv
import json
import requests
from flask import make_response
from bson import json_util
from bson.objectid import ObjectId
from response import make_json_response
import pandas as pd

from database import db

def get_by_id(id, collection):
    cursor = collection.find_one({"_id": ObjectId(id)})
    return make_json_response(json_util.dumps(cursor), 200)