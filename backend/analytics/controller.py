from .services import *
from flask import Blueprint, request
from response import unsupported_method

analytics_blueprint = Blueprint("analytics", __name__)

@analytics_blueprint.route("/<aggregate_key>/<id>/<date>", methods=['GET'])
def getAggregate(aggregate_key, id, date):
    if request.method == "GET":
        return get_fund_aggregate(id, date, aggregate_key)
    else:
        return unsupported_method()
    
@analytics_blueprint.route("/<lowerDate>/<upperDate>", methods=['GET'])
def getTotalMarketValue(lowerDate, upperDate):
    if request.method == "GET":
        return get_total_market_value(lowerDate, upperDate)
    else:
        return unsupported_method()