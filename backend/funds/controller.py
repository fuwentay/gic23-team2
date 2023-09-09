from .services import *
from flask import Blueprint, request
from database import db
from response import unsupported_method

funds_blueprint = Blueprint("funds", __name__)
positionsCollection = db.positions

@funds_blueprint.route("/<id>/instruments/<instrumentId>", methods=['GET'])
def getById(id, instrumentId):
    if request.method == "GET":
        return get_by_fund_instrument_id(id, instrumentId, positionsCollection)
    else:
        return unsupported_method()

@funds_blueprint.route("/<id>/refresh", methods=['POST'])
def refresh(id):
    if request.method == "POST":
        return refresh_by_id(id, positionsCollection)
    else:
        return unsupported_method()