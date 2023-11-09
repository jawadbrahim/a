from flask import Blueprint, request
from project.feature.food_category.americanfoods.controller import create_americanfood, get_americanfoods_list, update_americanfoods, delete_americanfoods, get_americanfood_single
from .error_handler import handle_americanfood_exceptions

americanfoods_bp = Blueprint("americanfoods", __name__, url_prefix="/americanfoods")

handle_americanfood_exceptions(americanfoods_bp)

@americanfoods_bp.route("/", methods=["POST", "GET"])
def americanfoods():
    if request.method == "POST":
        return create_americanfood()
    elif request.method == "GET":
        return get_americanfoods_list()

@americanfoods_bp.route("/<int:americanfood_id>", methods=["PUT"])
def update_americanfood(americanfood_id):
    return update_americanfoods(americanfood_id)

@americanfoods_bp.route("/<int:americanfood_id>", methods=["GET"])
def get_americanfood(americanfood_id):
    return get_americanfood_single(americanfood_id)

@americanfoods_bp.route("/<int:americanfood_id>", methods=["DELETE"])
def delete_americanfood(americanfood_id):
    return delete_americanfoods(americanfood_id)
