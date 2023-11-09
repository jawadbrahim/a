from flask import Blueprint, request
from project.feature.food_category.sauces.controller import create_sauce, get_sauces_list, update_sauces, delete_sauces, get_sauce_single
from .error_handler import handle_sauce_exceptions

sauces_bp = Blueprint("sauces", __name__, url_prefix="/sauces")

handle_sauce_exceptions(sauces_bp)

@sauces_bp.route("/", methods=["POST", "GET"])
def sauces():
    if request.method == "POST":
        return create_sauce()
    elif request.method == "GET":
        return get_sauces_list()

@sauces_bp.route("/<int:sauce_id>", methods=["PUT"])
def update_sauce(sauce_id):
    return update_sauces(sauce_id)

@sauces_bp.route("/<int:sauce_id>", methods=["GET"])
def get_sauce(sauce_id):
    return get_sauce_single(sauce_id)

@sauces_bp.route("/<int:sauce_id>", methods=["DELETE"])
def delete_sauce(sauce_id):
    return delete_sauces(sauce_id)
