from flask import Blueprint, request
from project.feature.food_category.africanfoods.controller import create_africanfood, get_africanfoods_list, update_africanfoods, delete_africanfoods, get_africanfood_single
from .error_handler import handle_africanfood_exceptions

africanfoods_bp = Blueprint("africanfoods", __name__, url_prefix="/africanfoods")

handle_africanfood_exceptions(africanfoods_bp)

@africanfoods_bp.route("/", methods=["POST", "GET"])
def africanfoods():
    if request.method == "POST":
        return create_africanfood()
    elif request.method == "GET":
        return get_africanfoods_list()

@africanfoods_bp.route("/<int:africanfood_id>", methods=["PUT"])
def update_africanfood(africanfood_id):
    return update_africanfoods(africanfood_id)

@africanfoods_bp.route("/<int:africanfood_id>", methods=["GET"])
def get_africanfood(africanfood_id):
    return get_africanfood_single(africanfood_id)

@africanfoods_bp.route("/<int:africanfood_id>", methods=["DELETE"])
def delete_africanfood(africanfood_id):
    return delete_africanfoods(africanfood_id)
