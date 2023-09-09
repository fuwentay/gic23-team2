from .services import *
from flask import Blueprint, request
from database import db

instruments_blueprint = Blueprint("instruments", __name__)
collection = db.instruments

@instruments_blueprint.route("/", methods = ["GET"])
def index():
    if request.method == "GET":
        return get_all(collection)
    else:
        return unsupported_method()

@instruments_blueprint.route("/<id>", methods=['GET', 'PUT'])
def idOperations(id):
    if request.method == "GET":
        return get_by_id(id, collection)
    elif request.method == "PUT":
        body = request.json()
        return update_by_id(id, body, collection)
    else:
        return unsupported_method()