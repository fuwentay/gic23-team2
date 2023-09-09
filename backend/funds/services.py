import csv
import json
import requests
from flask import make_response
from bson import json_util
from bson.objectid import ObjectId
from response import make_json_response

from database import db

def get_by_fund_instrument_id(fundId, instrumentId, positionsCollection):
    cursor = positionsCollection.find({"fundId": fundId, "instrumentId": instrumentId})
    return make_json_response(json_util.dumps(cursor), 200)

def refresh_by_id(fundId, positionsCollection):
    # TODO
    
    return make_json_response({}, 400)

def deleteStaleData(fundId):
    # TODO
    cursor = positionsCollection.find({"fundId": fundId})
