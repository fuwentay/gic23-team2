from .services import *
from flask import Blueprint, request
from database import db

price_values_blueprint = Blueprint("price_values", __name__)
priceCollection = db.price
instrumentsCollection = db.instruments

@price_values_blueprint.route("/<id>", methods=['GET'])
def getById(id):
    if request.method == "GET":
        return get_prices_by_id(id, priceCollection, instrumentsCollection)
    else:
        return unsupported_method()