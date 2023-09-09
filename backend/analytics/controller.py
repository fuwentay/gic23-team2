from .services import *
from flask import Blueprint, request
from database import db
from response import unsupported_method

analytics_blueprint = Blueprint("analytics", __name__)
positionsCollection = db.positions
priceCollection = db.price

@analytics_blueprint.route("/<aggregate_key>/<id>/<date>", methods=['GET'])
def getAggregate(aggregate_key, id, date):
    if request.method == "GET":
        return get_fund_aggregate(id, date, aggregate_key, positionsCollection, priceCollection)
    else:
        return unsupported_method()