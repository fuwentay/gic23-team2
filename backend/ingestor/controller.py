from .services import *
from flask import Blueprint, request
from database import db

ingestor_blueprint = Blueprint("instruments", __name__)
collection = db.instruments

@ingestor_blueprint.route("/", methods = ["GET"])
def index():
    if request.method == "GET":
        return get_all(collection)
    else:
        return "hello"

@ingestor_blueprint.route("/<id>", methods=['GET'])
def getById(id):
    if request.method == "GET":
        return get_by_id(id, collection)
    else:
        return unsupported_method()

@ingestor_blueprint.route("/<id>", methods=["PUT"])
def updateById(id):
    if request.method == "PUT":
        return insert_from_file_pd(request, collection)
    else:
        return unsupported_method()

@ingestor_blueprint.route("/insertFromApi", methods=["POST"])
def insertFromApi():
    if request.method == "POST":
        return insert_from_api(request, collection)
    else:
        return unsupported_method()

@ingestor_blueprint.route("/deleteAll", methods=["POST"])
def deleteAll():
    if request.method == "POST":
        return delete_all(collection)
    else:
        return unsupported_method()