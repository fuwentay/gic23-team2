from bson import json_util
from bson.objectid import ObjectId
from response import make_json_response
from ingestor.services import csv_to_db
from ingestor.fileUtils import *

from database import db
fundsCollection = db.funds

def get_by_fund_instrument_id(fundId, instrumentId, positionsCollection):
    cursor = positionsCollection.find({"fundId": fundId, "instrumentId": instrumentId})
    return make_json_response(json_util.dumps(cursor), 200)

def get_all_funds():
    cursor = fundsCollection.find()
    return make_json_response(json_util.dumps(cursor), 200)

def refresh_by_id(fundIdToRefresh, positionsCollection):
    new_input_files = get_input_files()
    positions_to_delete = []
    for fileName in new_input_files:
        fundName = get_fund_name(fileName)
        fundId = get_fund_id(fundName)
        if fundId != fundIdToRefresh:
            continue
        reportedDate = get_reported_date(fileName)
        positions_to_delete.append({ fundId, reportedDate })

    delete_stale_positions(positions_to_delete, positionsCollection)
    csv_to_db(positionsCollection)

    return make_json_response({}, 400)

def delete_stale_positions(positions_to_delete, positionsCollection):
    deleteManyResult = positionsCollection.delete_many({"$or": positions_to_delete})
    print(deleteManyResult)