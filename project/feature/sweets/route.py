from project.feature.sweets.controller import add_get_sweets,get_sweets,update_sweets,delete_sweets
from flask import request
from main import app

@app.route("/sweet", methods=["POST", "GET"])
def sweets():
    return add_get_sweets()

@app.route("/sweets/<int:sweet_id>", methods=["PUT", "GET", "DELETE"])
def sweet(sweet_id):
    if request.method == "PUT":
        return update_sweets(sweet_id)
    elif request.method == "GET":
        return get_sweets(sweet_id)
    elif request.method == "DELETE":
        return delete_sweets(sweet_id)