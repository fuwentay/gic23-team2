from flask import make_response
from bson import json_util
from .fileParser import *
from .fileUtils import *
from response import make_json_response
import pandas as pd
import os
import shutil
from database import db
from dateutil import parser
from datetime import datetime
import sqlite3

collection2 = db.chatbot_input
collection_f = db.fund
instrumentsCollection = db.instruments

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

# def get_fund_id(file_path):
#     dictFund = {'Trustmind':1, 'Virtous':2, 'Wallington':3, 'Gohen':4, 'Catalysm':5, 'Belaware': 6, 'Whitestone': 7, 'Leeder': 8, 'Magnum': 9, 'Applebead': 10}
#     for i in dictFund:
#         if i in file_path:
#             return dictFund[i]
        
# def getFund(file_path):
#     dictFund = {'Trustmind':1, 'Virtous':2, 'Wallington':3, 'Gohen':4, 'Catalysm':5, 'Belaware': 6, 'Whitestone': 7, 'Leeder': 8, 'Magnum': 9, 'Applebead': 10}
#     for i in dictFund:
#         if i in file_path:
#             return i
    

# determine instrumentId
def mapInstrumentType(instrument_type):
    dictInstrument = {'Equities': 1, 'Government Bond': 2, 'CASH': 3}
    return dictInstrument.get(instrument_type, None)

def map_instrument_id(symbol):
    document = instrumentsCollection.find_one({ "symbol": symbol })
    if document:
        return document["_id"]
    else:
        return instrumentsCollection.find_one({ "isinCode": symbol })


def get_reported_date(file_path):
    split_path = file_path.split(".")[-2]
    splitted_path = split_path.split()[0]
    try:
        date = parser.parse(splitted_path)
        datestr = date.strftime("%Y-%m-%d")
        
        return datestr
    except ValueError:
        day, month, year = splitted_path.split("_")

        if int(month) > 12:
            temp = day
            day = month
            month = temp

        # Construct a date string in the "yyyy-mm-dd" format
        formatted_date_str = f"{year}-{month}-{day}"

        # Parse the formatted date string
        date = parser.parse(formatted_date_str)
        datestr = date.strftime("%Y-%m-%d")
        return datestr


def read_from_csv(file_path):
    csv_file_path = file_path  # Replace with the path to your CSV file

    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file_path)

    # Create a dictionary for renaming columns
    column_mapping = {'FINANCIAL TYPE': 'instrumentType', 'SYMBOL': 'symbol', 'SECURITY NAME': 'instrumentName', 'PRICE': 'price', 'QUANTITY': 'quantity', 'REALISED P/L': 'realisedProfitLoss', 'MARKET VALUE': 'marketValue'}

    # Use the rename method to rename columns
    df.rename(columns=column_mapping, inplace=True)

    # Adding fundId attribute
    new_column_header_fundId = 'fundId'
    new_column_value_fundId = get_fund_id(file_path, collection_f)
    df[new_column_header_fundId] = new_column_value_fundId

    # Add fund attribute
    new_column_header_fund = 'fund'
    new_column_value_fund = get_fund_name(file_path)
    df[new_column_header_fund] = new_column_value_fund 

    # Adding reportedDate attribute
    new_column_header_date = 'reportedDate'
    new_column_value_date = get_reported_date(file_path)
    df[new_column_header_date] = new_column_value_date

    # Adding createdAt and modifiedAt attribute
    new_column_header_createdAt = 'createdAt'
    new_column_header_modifiedAt = 'modifiedAt'
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime('%Y-%m-%dT%H:%M:%S')
    new_column_value_createdmodified = formatted_datetime  
    df[new_column_header_createdAt] = new_column_value_createdmodified
    df[new_column_header_modifiedAt] = new_column_value_createdmodified

    # Adding instrumentId attribute
    df['instrumentId'] = df['symbol'].apply(map_instrument_id)

    data_dict = df.to_dict(orient='records')

    destination_path = os.path.join(os.path.dirname(__file__), "../inputs/expired")
    shutil.move(file_path, destination_path)

    return data_dict


def csv_to_db(collection):
    folder_path = get_input_folder()
    input_files = get_input_files()
    
    for filename in input_files:
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            json_file = read_from_csv(file_path)
            collection.insert_many(json_file)
            # print(f"Uploaded: {filename}")
    return make_json_response("Uploaded successfully", 500)


def parse_and_insert_instrument(rows, instrumentsCollection, instrumentType):    
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
    for i in range(len(rows)):
        rows[i] = {key_mapping.get(key, key): value for key, value in rows[i].items()}
        rows[i]["createdAt"] = datetime.now()
        rows[i]["modifiedAt"] = datetime.now()
        rows[i]["instrumentType"] = instrumentType
    insertManyResult = instrumentsCollection.insert_many(rows)
    insertedRowsCursor = instrumentsCollection.find({"_id": {"$in": insertManyResult.inserted_ids}})
    
    return json_util.dumps(list(insertedRowsCursor))    

def parse_and_insert_price(rows, priceCollection): 
    key_mapping = {
        'DATETIME': 'reportedDate', 
        'ISIN': 'isinCode', 
        'PRICE': "unitPrice",
        'SYMBOL': "symbol"
    }
    
    for i in range(len(rows)):
        rows[i] = {key_mapping.get(key, key): value for key, value in rows[i].items()}
        rows[i]["createdAt"] = datetime.now()
        rows[i]["modifiedAt"] = datetime.now()
    insertManyResult = priceCollection.insert_many(rows)
    insertedRowsCursor = priceCollection.find({"_id": {"$in": insertManyResult.inserted_ids}})
    
    return json_util.dumps(list(insertedRowsCursor))   

# Calculations of Market Value, Investment Return

def delete_all(collection):
    try:
        result = collection.delete_many({})
        deleted_count = result.deleted_count
        return make_json_response(f"Deleted {deleted_count} documents successfully", 200)
    except Exception as e:
        return make_json_response(str(e), 500)

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