from bson import json_util
from bson.objectid import ObjectId
from response import make_json_response

def get_fund_aggregate(fundId, upperBoundDate, aggregateKey, positionsCollection, priceCollection):
    pipeline = [
        {
            "$match": {
                # "fundId": fundId,
                "reportedDate": {"$lt": upperBoundDate}
            }
        }
    ]

    match_result = list(positionsCollection.aggregate(pipeline))
    aggregated_dict = {}
    for doc in match_result:
        if doc[aggregateKey] in aggregated_dict:
            if doc["instrumentType"] == "CASH":
                aggregated_dict[doc[aggregateKey]] += doc["marketValue"]
                continue
            # aggregated_dict[doc[aggregateKey]] += doc["quantity"] * get_latest_instrument_price(doc, upperBoundDate, priceCollection)
            aggregated_dict[doc[aggregateKey]] += doc["marketValue"]
        else:
            if doc["instrumentType"] == "CASH":
                aggregated_dict[doc[aggregateKey]] = doc["marketValue"]
                continue
            # aggregated_dict[doc[aggregateKey]] = doc["quantity"] * get_latest_instrument_price(doc, upperBoundDate, priceCollection)
            aggregated_dict[doc[aggregateKey]] = doc["marketValue"]

    return make_json_response(aggregated_dict, 200)

def get_latest_instrument_price(document, upperBoundDate, priceCollection):
    pipeline = [
        {
            "$match": {
                "$and": [
                    {
                        "$or": [
                            { 
                                "isinCode": document["isinCode"] if "isinCode" in document else document["symbol"]
                            },
                            {
                                "symbol": document["symbol"] if "symbol" in document else document["isinCode"]
                            }
                        ]
                    },
                    {
                        "reportedDate": {"$lt": upperBoundDate}
                    }
                ]
            }
        },
        {
            "$sort": {
                "date": -1  
            }
        },
        {
            "$limit": 1
        }
    ]

    result = list(priceCollection.aggregate(pipeline))
    try:
        return result[0]["unitPrice"]
    except:
        print(document)

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
