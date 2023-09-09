from .services import *
from flask import Blueprint, request
from database import db

price_values_blueprint = Blueprint("price_values", __name__)
positionsCollection = db.positions

@price_values_blueprint.route("/<id>/instruments/<instrumentId>", methods=['GET'])
def getById(id, instrumentId):
    if request.method == "GET":
        return get_by_fund_instrument_id(id, instrumentId, positionsCollection)
    else:
        return unsupported_method()