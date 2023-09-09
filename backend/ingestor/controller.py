from .services import *
from flask import Blueprint, request
from database import db

ingestor_blueprint = Blueprint("ingestor", __name__)
instrumentsCollection = db.instruments
priceCollection = db.price

@ingestor_blueprint.route("/insertFromCsv", methods=["POST"])
def insertFromFilePD():
    if request.method == "POST":
        return insert_from_file_pd(request, instrumentsCollection, positionsCollection)
    else:
        return unsupported_method()

@ingestor_blueprint.route("/insertFromApi", methods=["POST"])
def insertFromApi():
    if request.method == "POST":
        return insert_from_api(request, instrumentsCollection, positionsCollection)
    else:
        return unsupported_method()

@ingestor_blueprint.route("/insertFromDb", methods=["GET"])
def insertFromDb():
    if request.method == "GET":
        return insert_from_db("/Users/solivagant_ss/Documents/GitHub/2023-app-2/backend/inputs/master-reference.db", instrumentsCollection, priceCollection)
    else:
        return unsupported_method()

@ingestor_blueprint.route("/deleteAll", methods=["POST"])
def deleteAll():
    if request.method == "POST":
        return delete_all(collection)
    else:
        return unsupported_method()