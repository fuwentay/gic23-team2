import csv
import json
import requests
from flask import make_response
from bson import json_util
from bson.objectid import ObjectId
from .fileParser import *
from response import make_json_response
import pandas as pd
import os
from database import db
from dateutil import parser
from datetime import datetime

collection2 = db.chatbot_input
collection_p = db.positions

def getFundId(file_path):
    dictFund = {'Trustmind':1, 'Virtous':2, 'Wallington':3, 'Gohen':4, 'Catalysm':5, 'Belaware': 6, 'Whitestone': 7, 'Leeder': 8, 'Magnum': 9, 'Applebead': 10}
    for i in dictFund:
        if i in file_path:
            return dictFund[i]





# determine instrumentId
def mapInstrumentType(instrument_type):
    dictInstrument = {'Equities': 1, 'Government Bond': 2, 'CASH': 3}
    return dictInstrument.get(instrument_type, None)


def getReportedDate(file_path):
    split_path = file_path.split(".")[1]
    splitted_path = split_path.split()[0]
    date = parser.parse(splitted_path)
    datestr = date.strftime("%Y-%m-%d")
    return datestr


def read_from_csv(file_path):
    csv_file_path = file_path  # Replace with the path to your CSV file

    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file_path)

    # Create a dictionary for renaming columns
    column_mapping = {'FINANCIAL TYPE': 'financialType', 'SYMBOL': 'symbol', 'SECURITY NAME': 'securityName', 'PRICE': 'price', 'QUANTITY': 'quantity', 'REALISED P/L': 'realisedProfitLoss', 'MARKET VALUE': 'marketValue'}

    # Use the rename method to rename columns
    df.rename(columns=column_mapping, inplace=True)

    # Adding fundId attribute
    new_column_header = 'fundId'
    new_column_value = getFundId(file_path)
    df[new_column_header] = new_column_value

    # Adding instrumentId attribute
    df['instrumentId'] = df['financialType'].apply(mapInstrumentType)

    # Adding reportedDate attribute
    new_column_header_date = 'reportedDate'
    new_column_value_date = getReportedDate(file_path)
    df[new_column_header_date] = new_column_value_date

    # Adding createdAt and modifiedAt attribute
    new_column_header_createdAt = 'createdAt'
    new_column_header_modifiedAt = 'modifiedAt'
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime('%Y-%m-%dT%H:%M:%S')
    new_column_value_createdmodified = formatted_datetime  
    df[new_column_header_createdAt] = new_column_value_createdmodified
    df[new_column_header_modifiedAt] = new_column_value_createdmodified

    data_dict = df.to_dict(orient='records')

    return data_dict


def csv_to_db(collection):
    # # Check if the folder path exists
    folder_path = "backend\inputs"
    if os.path.exists(folder_path):
        # Iterate through the files in the folder and upload them to MongoDB
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                json_file = read_from_csv(file_path)
                collection.insert_many(json_file)
                print(f"Uploaded: {filename}")
        return "Successful"
    else:
        print(f"The specified folder '{folder_path}' does not exist.")


def get_all(collection):
    cursor = collection.find()
    return make_json_response(json_util.dumps(cursor), 200)


def get_by_id(id, collection):
    cursor = collection.find_one({"_id": ObjectId(id)})
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




