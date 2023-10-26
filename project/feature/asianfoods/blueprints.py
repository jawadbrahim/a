from flask import Blueprint
asianfoods_bp=Blueprint("asianfoods",__name__,url_prefix="/asianfoods")
from project.feature.asianfoods.controller import add_get_asianfoods,update_asianfoods,get_asianfoods,delete_asianfoods
from.error_handler import handle_asianfood_exceptions


asianfoods_bp = Blueprint("asianfoods", __name__, url_prefix="/asianfoods")
handle_asianfood_exceptions(asianfoods_bp)
@asianfoods_bp.route("/", methods=["POST", "GET"])
def asianfood():
    return add_get_asianfoods()
@asianfoods_bp.route("/<int:asianfood_id>", methods=["PUT"])
def put_asianfood(asianfood_id):
    return update_asianfoods(asianfood_id)

@asianfoods_bp.route("/<int:asianfood_id>", methods=["GET"])
def get_asianfood(asianfood_id):
    return get_asianfoods(asianfood_id)

@asianfoods_bp.route("/<int:asianfood_id>", methods=["DELETE"])
def delete_asianfood(asianfood_id):
    return delete_asianfoods(asianfood_id)