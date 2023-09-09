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

def insert_from_db(file, instrumentsCollection, priceCollection):
    dbData = read_from_db(file)
    for tableName, tableData in dbData.items():
        if tableName == "bond_reference":
            insertedRows = parse_and_insert_instrument(tableData, instrumentsCollection, "Government Bond")
        elif tableName == "bond_prices":
            insertedRows = parse_and_insert_price(tableData, priceCollection)
        elif tableName == "equity_reference":
            insertedRows = parse_and_insert_instrument(tableData, instrumentsCollection, "Equity")
        elif tableName == "equity_prices":
            insertedRows = parse_and_insert_price(tableData, priceCollection)

    return make_json_response(insertedRows, 200)

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

def getFundId(file_path):
    dictFund = {'Trustmind':1, 'Virtous':2, 'Wallington':3, 'Gohen':4, 'Catalysm':5, 'Belaware': 6, 'Whitestone': 7, 'Leeder': 8, 'Magnum': 9, 'Applebead': 10}
    for i in dictFund:
        if i in file_path:
            return dictFund[i]
        
def getFund(file_path):
    dictFund = {'Trustmind':1, 'Virtous':2, 'Wallington':3, 'Gohen':4, 'Catalysm':5, 'Belaware': 6, 'Whitestone': 7, 'Leeder': 8, 'Magnum': 9, 'Applebead': 10}
    for i in dictFund:
        if i in file_path:
            return i

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
    column_mapping = {'FINANCIAL TYPE': 'instrumentType', 'SYMBOL': 'symbol', 'SECURITY NAME': 'securityName', 'PRICE': 'price', 'QUANTITY': 'quantity', 'REALISED P/L': 'realisedProfitLoss', 'MARKET VALUE': 'marketValue'}

    # Use the rename method to rename columns
    df.rename(columns=column_mapping, inplace=True)

    # Adding fundId attribute
    new_column_header_fundId = 'fundId'
    new_column_value_fundId = getFundId(file_path)
    df[new_column_header_fundId] = new_column_value_fundId

    # Add fund attribute
    new_column_header_fund = 'fund'
    new_column_value_fund = getFund(file_path)
    df[new_column_header_fund] = new_column_value_fund 

    # Adding instrumentId attribute
    df['instrumentId'] = df['instrumentType'].apply(mapInstrumentType)

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


def parse_and_insert_instrument(rows, collection, instrumentType):    
    key_mapping = {
        'SYMBOL': 'symbol',
        'COUNTRY': 'country',
        'SECURITY NAME': 'instrumentName',
        'SECTOR': 'sector',
        'INDUSTRY': 'industry',
        'CURRENCY': 'currency',
        'ISIN': 'isinCode',
        'SEDOL': 'sedolCode',
        'COUPON': 'coupon',
        'MATURITY DATE': 'maturityDate',
        'COUPON FREQUENCY': 'couponFrequency'
    }   
    instruments = {}
    for i in range(len(rows)):
        row = {key_mapping.get(key, key): value for key, value in rows[i].items()}
        instrumentName = get_instrument_name(row["instrumentName"])
        if instrumentName in instruments:
            continue
        del row["coupon"]
        del row["maturityDate"]
        del row["couponFrequency"]
        row["instrumentName"] = instrumentName
        row["createdAt"] = datetime.now()
        row["modifiedAt"] = datetime.now()
        row["instrumentType"] = instrumentType
        instruments[instrumentName] = row
    insertManyResult = collection.insert_many(list(instruments))
    insertedRowsCursor = collection.find({"_id": {"$in": insertManyResult.inserted_ids}})
    
    return json_util.dumps(list(insertedRowsCursor))    

def parse_and_insert_price(rows, collection): 
    key_mapping = {
        'DATETIME': 'reportedDate', 
        'ISIN': 'isinCode', 
        'PRICE': "unitPrice"
    }
    
    for i in range(len(rows)):
        rows[i] = {key_mapping.get(key, key): value for key, value in rows[i].items()}
        rows[i]["createdAt"] = datetime.now()
        rows[i]["modifiedAt"] = datetime.now()
    insertManyResult = collection.insert_many(rows)
    insertedRowsCursor = collection.find({"_id": {"$in": insertManyResult.inserted_ids}})
    
    return json_util.dumps(list(insertedRowsCursor))   

def get_instrument_name(securityName):
    percentIndex = find_first_digit_index(securityName)
    return securityName[:percentIndex-1]

def find_first_digit_index(s):
    for index, char in enumerate(s):
        if char.isdigit():
            return index
    return -1

# Calculations of Market Value, Investment Return

def delete_all(collection):
    try:
        result = collection.delete_many({})
        deleted_count = result.deleted_count
        return make_json_response(f"Deleted {deleted_count} documents successfully", 200)
    except Exception as e:
        return make_json_response(str(e), 500)


def unsupported_method():
    return make_json_response("Request type not supported", 400)

# # inserts pandas df to db.chatbot and json to db.ingest
# def insert_from_file_pd(request, collection):
#     if 'file' not in request.files:
#         return make_json_response("No file found in request.files", 400)
#     file = request.files['file']
#     if file.filename == '':
#         return make_json_response("No selected file", 400)
#     try:
#         df = pd.read_csv(file)
#         df["filename"] = file.filename
#         data_dict = df.to_dict(orient='records')
#         collection2.insert_many(data_dict)
#         file.seek(0)
#         file_contents_array = read_csv_from_file(file)
#         rows = transform_file_rows_to_objects(file_contents_array)

#         insertedRows = insert_and_get(rows, collection)
#         return make_json_response(insertedRows, 200)
#     except csv.Error:
#         return make_json_response("Invalid CSV format in the uploaded file", 400)


# def insert_and_get(rows, collection):    
#     insertManyResult = collection.insert_many(rows)
#     insertedRowsCursor = collection.find({"_id": {"$in": insertManyResult.inserted_ids}})
    
#     return json_util.dumps(list(insertedRowsCursor))