import csv
import json
import requests
from flask import make_response
from bson import json_util
from bson.objectid import ObjectId
from response import make_json_response

from database import db

def get_prices_by_id(instrumentId, priceCollection, instrumentsCollection):
    document = instrumentsCollection.find_one({"_id": ObjectId(instrumentId)})
    if not document:
        return make_json_response(json_util.dumps(cursor), 400)
    if document["instrumentType"] == "Equity":
        key = "symbol"  
    else:
        key = "isinCode"
    pricesCursor = priceCollection.find({key: document[key]}) # TODO - filter by last price of the month
    return make_json_response(json_util.dumps(pricesCursor), 200)
