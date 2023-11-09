from flask import Blueprint,request
from project.feature.food_category.arabicfoods.controller import create_arabicfood,get_arabicfoods_list, update_arabicfoods, delete_arabicfoods,get_arabicfood_single
from .error_handler import handle_arabicfood_exceptions

arabicfoods_bp = Blueprint("arabicfoods", __name__, url_prefix="/arabicfoods")

handle_arabicfood_exceptions(arabicfoods_bp)

@arabicfoods_bp.route("/", methods=["POST", "GET"])
def arabicfoods():
    if request.method == "POST":
        return create_arabicfood()
    elif request.method == "GET":
        return get_arabicfoods_list()

@arabicfoods_bp.route("/<int:arabicfood_id>", methods=["PUT"])
def update_arabicfood(arabicfood_id):
    return update_arabicfoods(arabicfood_id)

@arabicfoods_bp.route("/<int:arabicfood_id>", methods=["GET"])
def get_arabicfood(arabicfood_id):
    return get_arabicfood_single(arabicfood_id)

@arabicfoods_bp.route("/<int:arabicfood_id>", methods=["DELETE"])
def delete_arabicfood(arabicfood_id):
    return delete_arabicfoods(arabicfood_id)
