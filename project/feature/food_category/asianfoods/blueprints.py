from flask import Blueprint, request
from project.feature.food_category.asianfoods.controller import create_asianfood, get_asianfoods_list, update_asianfoods, delete_asianfoods, get_asianfood_single
from .error_handler import handle_asianfood_exceptions

asianfoods_bp = Blueprint("asianfoods", __name__, url_prefix="/asianfoods")

handle_asianfood_exceptions(asianfoods_bp)

@asianfoods_bp.route("/", methods=["POST", "GET"])
def asianfoods():
    if request.method == "POST":
        return create_asianfood()
    elif request.method == "GET":
        return get_asianfoods_list()

@asianfoods_bp.route("/<int:asianfood_id>", methods=["PUT"])
def update_asianfood(asianfood_id):
    return update_asianfoods(asianfood_id)

@asianfoods_bp.route("/<int:asianfood_id>", methods=["GET"])
def get_asianfood(asianfood_id):
    return get_asianfood_single(asianfood_id)

@asianfoods_bp.route("/<int:asianfood_id>", methods=["DELETE"])
def delete_asianfood(asianfood_id):
    return delete_asianfoods(asianfood_id)
