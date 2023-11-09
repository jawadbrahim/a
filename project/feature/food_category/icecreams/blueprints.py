from flask import Blueprint, request
from project.feature.food_category.icecreams.controller import create_icecream, get_icecreams_list, update_icecreams, delete_icecreams, get_icecream_single
from .error_handler import handle_icecream_exceptions

icecreams_bp = Blueprint("icecreams", __name__, url_prefix="/icecreams")

handle_icecream_exceptions(icecreams_bp)

@icecreams_bp.route("/", methods=["POST", "GET"])
def icecreams():
    if request.method == "POST":
        return create_icecream()
    elif request.method == "GET":
        return get_icecreams_list()

@icecreams_bp.route("/<int:icecream_id>", methods=["PUT"])
def update_icecream(icecream_id):
    return update_icecreams(icecream_id)

@icecreams_bp.route("/<int:icecream_id>", methods=["GET"])
def get_icecream(icecream_id):
    return get_icecream_single(icecream_id)

@icecreams_bp.route("/<int:icecream_id>", methods=["DELETE"])
def delete_icecream(icecream_id):
    return delete_icecreams(icecream_id)
