from flask import Blueprint, request
from project.feature.food_category.sweets.controller import create_sweet, get_sweets_list, update_sweets, delete_sweets, get_sweet_single
from .error_handler import handle_sweet_exceptions

sweets_bp = Blueprint("sweets", __name__, url_prefix="/sweets")

handle_sweet_exceptions(sweets_bp)

@sweets_bp.route("/", methods=["POST", "GET"])
def sweets():
    if request.method == "POST":
        return create_sweet()
    elif request.method == "GET":
        return get_sweets_list()

@sweets_bp.route("/<int:sweet_id>", methods=["PUT"])
def update_sweet(sweet_id):
    return update_sweets(sweet_id)

@sweets_bp.route("/<int:sweet_id>", methods=["GET"])
def get_sweet(sweet_id):
    return get_sweet_single(sweet_id)

@sweets_bp.route("/<int:sweet_id>", methods=["DELETE"])
def delete_sweet(sweet_id):
    return delete_sweets(sweet_id)
