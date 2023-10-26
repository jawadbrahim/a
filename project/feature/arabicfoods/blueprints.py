from flask import Blueprint,request
from project.feature.arabicfoods.controller import add_get_arabicfoods, get_arabicfoods, update_arabicfoods, delete_arabicfoods
from .error_handler import handle_arabicfood_exceptions

arabicfoods_bp = Blueprint("arabicfoods", __name__, url_prefix="/arabicfoods")
handle_arabicfood_exceptions(arabicfoods_bp)

@arabicfoods_bp.route("/", methods=["GET", "POST"])
def arabicfoods():
    return add_get_arabicfoods()

@arabicfoods_bp.route("/<int:arabicfood_id>", methods=["PUT"])
def put_arabicfood(arabicfood_id):
    return update_arabicfoods(arabicfood_id)

@arabicfoods_bp.route("/<int:arabicfood_id>", methods=["GET"])
def get_arabicfood(arabicfood_id):
    return get_arabicfoods(arabicfood_id)

@arabicfoods_bp.route("/<int:arabicfood_id>", methods=["DELETE"])
def delete_arabicfood(arabicfood_id):
    return delete_arabicfoods(arabicfood_id)