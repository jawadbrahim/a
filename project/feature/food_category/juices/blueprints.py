from flask import Blueprint, request
from project.feature.food_category.juices.controller import create_juice, get_juices_list, update_juices, delete_juices, get_juice_single
from .error_handler import handle_juice_exceptions

juices_bp = Blueprint("juices", __name__, url_prefix="/juices")

handle_juice_exceptions(juices_bp)

@juices_bp.route("/", methods=["POST", "GET"])
def juices():
    if request.method == "POST":
        return create_juice()
    elif request.method == "GET":
        return get_juices_list()

@juices_bp.route("/<int:juice_id>", methods=["PUT"])
def update_juice(juice_id):
    return update_juices(juice_id)

@juices_bp.route("/<int:juice_id>", methods=["GET"])
def get_juice(juice_id):
    return get_juice_single(juice_id)

@juices_bp.route("/<int:juice_id>", methods=["DELETE"])
def delete_juice(juice_id):
    return delete_juices(juice_id)
