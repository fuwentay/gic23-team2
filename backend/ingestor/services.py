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
from datetime import datetime
from database import db

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


def delete_all(collection):
    try:
        result = collection.delete_many({})
        deleted_count = result.deleted_count
        return make_json_response(f"Deleted {deleted_count} documents successfully", 200)
    except Exception as e:
        return make_json_response(str(e), 500)


def unsupported_method():
    return make_json_response("Request type not supported", 400)


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
    for i in range(len(rows)):
        rows[i] = {key_mapping.get(key, key): value for key, value in rows[i].items()}
        rows[i]["createdAt"] = datetime.now()
        rows[i]["modifiedAt"] = datetime.now()
        rows[i]["instrumentType"] = instrumentType
    insertManyResult = collection.insert_many(rows)
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

# Calculations of Market Value, Investment Return