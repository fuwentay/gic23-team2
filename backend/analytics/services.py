import csv
import json
from bson import json_util
from bson.objectid import ObjectId
from response import make_json_response

from database import db
collection2 = db.positions

def get_all(collection):
    cursor = collection.find()
    return make_json_response(json_util.dumps(cursor), 200)

def get_by_id(id, collection):
    cursor = collection.find_one({"_id": ObjectId(id)})
    return make_json_response(json_util.dumps(cursor), 200)

def get_by_instrument(instrument, collection):
    cursor = collection.find_one({"instrumentId": instrument})
    return make_json_response(json_util.dumps(cursor), 200)

def get_by_country(country, collection):
    cursor = collection.find_one({"country": country})
    return make_json_response(json_util.dumps(cursor), 200)

def get_by_sector(sector, collection):
    cursor = collection.find_one({"sector": sector})
    return make_json_response(json_util.dumps(cursor), 200)

def get_by_fund(fund, collection):
    cursor = collection.find_one({"fundId": fund})
    return make_json_response(json_util.dumps(cursor), 200)

# TODO: Datetime treatment?
def get_by_date(date, collection):
    cursor = collection.find_one({"date": date})
    return make_json_response(json_util.dumps(cursor), 200)

# TODO: Datetime treatment?
def get_by_date_range(start_date, end_date, collection):
    cursor = collection.find({"start_date": start_date, "end_date": end_date})
    return make_json_response(json_util.dumps(cursor), 200)

def get_top_N_funds(frequency, date, N, collection):
    cursor = collection.find({"date": date})
    cursor = collection.find(
        {
            "date": date
        }
    ).sort("investment_return", -1).limit(N)
    return make_json_response(json_util.dumps(cursor), 200)

def delete_all(collection):
    try:
        result = collection.delete_many({})
        deleted_count = result.deleted_count
        return make_json_response(f"Deleted {deleted_count} documents successfully", 200)
    except Exception as e:
        return make_json_response(str(e), 500)
