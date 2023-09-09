from .services import *
from flask import Blueprint, request
from database import db

ingestor_blueprint = Blueprint("ingestor", __name__)
collection = db.instruments

@ingestor_blueprint.route("/<id>", methods=['GET'])
def getById(id):
    if request.method == "GET":
        return get_by_id(id, collection)
    else:
        return unsupported_method()