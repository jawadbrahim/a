from flask import Blueprint
from project.feature.americanfoods.controller import add_get_americanfoods, get_americanfoods, update_americanfoods, delete_americanfoods
from .error_handler import handle_americanfood_exceptions



americanfoods_bp = Blueprint("americanfoods", __name__, url_prefix="/americanfoods")
handle_americanfood_exceptions(americanfoods_bp)
@americanfoods_bp.route("/", methods=["GET", "POST"])
def americanfoods():
    return add_get_americanfoods()

@americanfoods_bp.route("/<int:americanfood_id>", methods=["PUT"])
def put_americanfood(americanfood_id):
    return update_americanfoods(americanfood_id)

@americanfoods_bp.route("/<int:americanfood_id>", methods=["GET"])
def get_americanfood(americanfood_id):
    return get_americanfoods(americanfood_id)

@americanfoods_bp.route("/<int:americanfood_id>", methods=["DELETE"])
def delete_americanfood(americanfood_id):
    return delete_americanfoods(americanfood_id)