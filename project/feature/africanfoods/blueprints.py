from flask import Blueprint
from .error_handler import handle_africanfood_exceptions
from project.feature.africanfoods.controller import add_get_africanfoods,get_africanfoods,delete_africanfoods,update_africanfoods


africanfoods_bp=Blueprint("africanfoods",__name__,url_prefix="/africanfoods")
handle_africanfood_exceptions(africanfoods_bp)
@africanfoods_bp.route("/", methods=["POST", "GET"])
def africanfood():
    return add_get_africanfoods()

@africanfoods_bp.route("/<int:africanfood_id>", methods=["PUT"])
def put_africanfood(africanfood_id):
    return update_africanfoods(africanfood_id)

@africanfoods_bp.route("/<int:africanfood_id>", methods=["GET"])
def get_africanfood(africanfood_id):
    return get_africanfoods(africanfood_id)

@africanfoods_bp.route("/<int:africanfood_id>", methods=["DELETE"])
def delete_africanfood(africanfood_id):
    return delete_africanfoods(africanfood_id)