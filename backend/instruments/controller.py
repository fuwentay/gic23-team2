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
        return "hello"

@instruments_blueprint.route("/<id>", methods=['GET'])
def getById(id):
    if request.method == "GET":
        return get_by_id(id, collection)
    else:
        return unsupported_method()

@instruments_blueprint.route("/<id>", methods=["PUT"])
def updateById():
    if request.method == "PUT":
        return delete_all(collection)
    else:
        return unsupported_method()