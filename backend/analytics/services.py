import csv
import json
import requests
from flask import make_response
from bson import json_util
from bson.objectid import ObjectId
from .fileParser import *
from response import make_json_response
import pandas as pd

from database import db
collection2 = db.positions

def get_all(collection):
    cursor = collection.find()
    return make_json_response(json_util.dumps(cursor), 200)


def get_by_id(id, collection):
    cursor = collection.find_one({"_id": ObjectId(id)})
    return make_json_response(json_util.dumps(cursor), 200)

def get_by_instrument(instrument, collection):
    cursor = collection.find_one({"instrument_ID": instrument})
    return make_json_response(json_util.dumps(cursor), 200)

def get_by_country(country, collection):
    cursor = collection.find_one({"country": country})
    return make_json_response(json_util.dumps(cursor), 200)

def get_by_sector(sector, collection):
    cursor = collection.find_one({"sector": sector})
    return make_json_response(json_util.dumps(cursor), 200)

def get_by_fund(fund, collection):
    cursor = collection.find_one({"fund": fund})
    return make_json_response(json_util.dumps(cursor), 200)

# TODO: Datetime treatment
def get_by_sector(date, collection):
    cursor = collection.find_one({"date": date})
    return make_json_response(json_util.dumps(cursor), 200)

# reuse function from entitites?
def getTotalMarketValue():
    cursor = collection2.aggregate([{"$group" : {"_id" : "$country", "totalMarketValue" : {"$sum" : "$market_value"}}}])
    return make_json_response(json_util.dumps(cursor), 200)

# inserts pandas df to db.chatbot and json to db.ingest
def insert_from_file_pd(request, collection):
    if 'file' not in request.files:
        return make_json_response("No file found in request.files", 400)
    file = request.files['file']
    if file.filename == '':
        return make_json_response("No selected file", 400)
    try:
        df = pd.read_csv(file)
        df["filename"] = file.filename
        data_dict = df.to_dict(orient='records')
        collection2.insert_many(data_dict)
        file.seek(0)
        file_contents_array = read_csv_from_file(file)
        rows = transform_file_rows_to_objects(file_contents_array)

        insertedRows = insert_and_get(rows, collection)
        return make_json_response(insertedRows, 200)
    except csv.Error:
        return make_json_response("Invalid CSV format in the uploaded file", 400)
    

# def insert_from_file(request, collection):
#     if 'file' not in request.files:
#         return make_json_response("No file found in request.files", 400)
#     file = request.files['file']
#     if file.filename == '':
#         return make_json_response("No selected file", 400)
#     try:
#         file_contents_array = read_csv_from_file(file)
#         rows = transform_file_rows_to_objects(file_contents_array)

#         insertedRows = insert_and_get(rows, collection)
#         return make_json_response(insertedRows, 200)
#     except csv.Error:
#         return make_json_response("Invalid CSV format in the uploaded file", 400)


def insert_from_api(request, collection):
    json = request.get_json()
    url = json['url']
    headers = {
        'Accept': 'application/json', 
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
    }
    response = requests.get(url, headers=headers)

    # TODO: see what the data structure is, may need to convert to pandas df. this is to add url attribute to data and send to collection2
    # response_json2 = response.json()
    # insert_and_get(response_json2['data'], collection2)

    response_json = response.json()
    insertedRows = insert_and_get(response_json['data'], collection)
    return make_json_response(insertedRows, 200)


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
