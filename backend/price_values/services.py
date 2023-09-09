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
        return make_json_response(json_util.dumps(document), 400)
    if document["instrumentType"] == "Equity":
        key = "symbol"  
    else:
        key = "isinCode"

    pipeline = [
        {
            "$match": {
                key: document[key], 
            }
        },
        {
            "$addFields": {
                "reportedDate": {
                    "$toDate": "$reportedDate" 
                }
            }
        },
        {
            "$group": {
                "_id": {
                    "year": {"$year": "$reportedDate"},
                    "month": {"$month": "$reportedDate"}
                },
                "maxDate": {"$max": "$reportedDate"},
                "documentId": {"$last": "$_id"}
            }
        },
        {
            "$project": {
                "_id": "$documentId",
                "reportedDate": "$maxDate"
            }
        }
    ]
    last_documents_of_each_month = list(priceCollection.aggregate(pipeline))
    return make_json_response(json_util.dumps(last_documents_of_each_month), 200)
