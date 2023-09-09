import csv
import json
import requests
from flask import make_response
from bson import json_util
from bson.objectid import ObjectId
from .fileParser import *
from response import make_json_response
import pandas as pd
import sqlite3

from database import db
collection2 = db.chatbot_input


# inserts pandas df to db.chatbot and json to db.ingest
def insert_from_file_pd(request, instrumentsCollection, positionsCollection):
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

        insertedRows = insert_and_get(rows, instrumentsCollection)
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

def read_from_db(dbFile):
    data = {}
    
    # Connect to the SQLite database
    conn = sqlite3.connect(dbFile)
    cursor = conn.cursor()
    
    # Get a list of all table names in the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    for table in tables:
        table_name = table[0]
        data[table_name] = []
        
        # Get column names for the current table
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [col[1] for col in cursor.fetchall()]
        
        # Fetch all rows from the current table
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        
        for row in rows:
            row_dict = {}
            for i, column_name in enumerate(columns):
                row_dict[column_name] = row[i]
            data[table_name].append(row_dict)
    
    # Close the database connection
    conn.close()
    
    return data

def insert_from_db(file, instrumentsCollection = None, priceCollection = None):
    dbData = read_from_db(file)
    for tableName, tableData in dbData.items():
        print(tableName)
        print(tableData[0])
        if tableName == "bond_reference":
            insertedRows = parse_and_insert_instrument(tableData, instrumentsCollection)
        elif tableName == "bond_prices":
            insertedRows = parse_and_insert_price(tableData, priceCollection)
        elif tableName == "equity_reference":
            insertedRows = parse_and_insert_instrument(tableData, instrumentsCollection)
        elif tableName == "equity_prices":
            insertedRows = parse_and_insert_price(tableData, priceCollection)

# def insert_from_api(request, collection):
#     json = request.get_json()
#     url = json['url']
#     headers = {
#         'Accept': 'application/json', 
#         'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
#     }
#     response = requests.get(url, headers=headers)

#     # TODO: see what the data structure is, may need to convert to pandas df. this is to add url attribute to data and send to collection2
#     # response_json2 = response.json()
#     # insert_and_get(response_json2['data'], collection2)

#     response_json = response.json()
#     insertedRows = insert_and_get(response_json['data'], collection)
#     return make_json_response(insertedRows, 200)


def delete_all(collection):
    try:
        result = collection.delete_many({})
        deleted_count = result.deleted_count
        return make_json_response(f"Deleted {deleted_count} documents successfully", 200)
    except Exception as e:
        return make_json_response(str(e), 500)


def unsupported_method():
    return make_json_response("Request type not supported", 400)


def parse_and_insert_instrument(rows, collection):    
    key_mapping = {
        'DATETIME': 'reportedDate', 
        'ISIN': 'isinCode', 
        'PRICE': "unitPrice"
    }
    for i in range(len(rows)):
        rows[i] = {key_mapping.get(key, key): value for key, value in rows[i].items()}
    insertManyResult = db.test.insert_many(rows)
    # insertManyResult = collection.insert_many(rows)
    # insertedRowsCursor = collection.find({"_id": {"$in": insertManyResult.inserted_ids}})
    
    # return json_util.dumps(list(insertedRowsCursor))    
    return

def parse_and_insert_price(rows, collection): 
    key_mapping = {
        'SYMBOL': 'symbol',
        'COUNTRY': 'country',
        'SECURITY NAME': 'instrumentName',
        'SECTOR': 'sector',
        'INDUSTRY': 'industry',
        'CURRENCY': 'currency'
    }   
    for i in range(len(rows)):
        rows[i] = {key_mapping.get(key, key): value for key, value in rows[i].items()}
    insertManyResult = collection.insert_many(rows)
    # insertedRowsCursor = collection.find({"_id": {"$in": insertManyResult.inserted_ids}})
    
    # return json_util.dumps(list(insertedRowsCursor))    
    print(insertManyResult)
    return