from .services import *
from flask import Blueprint, request
from database import db

ingestor_blueprint = Blueprint("funds", __name__)
collection = db.positions

@ingestor_blueprint.route("/", methods = ["POST"])
def index():
    if request.method == "GET":
        return get_all(collection)
    else:
        return "hello"

@ingestor_blueprint.route("/<id>/instruments/<instrument_id>", methods=['GET'])
def getById(id, instrument_id):
    if request.method == "GET":
        return get_by_id(id, collection)
    else:
        return unsupported_method()