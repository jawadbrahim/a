from flask import Blueprint, request
from project.feature.food_category.europeanfoods.controller import create_europeanfood, get_europeanfoods_list, update_europeanfoods, delete_europeanfoods, get_europeanfood_single
from .error_handler import handle_europeanfood_exceptions

europeanfoods_bp = Blueprint("europeanfoods", __name__, url_prefix="/europeanfoods")

handle_europeanfood_exceptions(europeanfoods_bp)

@europeanfoods_bp.route("/", methods=["POST", "GET"])
def europeanfoods():
    if request.method == "POST":
        return create_europeanfood()
    elif request.method == "GET":
        return get_europeanfoods_list()

@europeanfoods_bp.route("/<int:europeanfood_id>", methods=["PUT"])
def update_europeanfood(europeanfood_id):
    return update_europeanfoods(europeanfood_id)

@europeanfoods_bp.route("/<int:europeanfood_id>", methods=["GET"])
def get_europeanfood(europeanfood_id):
    return get_europeanfood_single(europeanfood_id)

@europeanfoods_bp.route("/<int:europeanfood_id>", methods=["DELETE"])
def delete_europeanfood(europeanfood_id):
    return delete_europeanfoods(europeanfood_id)
