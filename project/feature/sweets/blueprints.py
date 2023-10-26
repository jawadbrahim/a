from flask import Blueprint
from .error_handler import handle_sweet_exceptions
from project.feature.sweets.controller import add_get_sweets,get_sweets,update_sweets,delete_sweets

sweets_bp=Blueprint("sweets",__name__,url_prefix="/sweets")
handle_sweet_exceptions(sweets_bp)
@sweets_bp.route("/", methods=["POST", "GET"])
def sweets():
    return add_get_sweets()

@sweets_bp.route("/<int:sweet_id>", methods=["PUT"])
def put_sweet(sweet_id):
    return update_sweets(sweet_id)

@sweets_bp.route("/<int:sweet_id>", methods=["GET"])
def get_sweet(sweet_id):
    return get_sweets(sweet_id)

@sweets_bp.route("/<int:sweet_id>", methods=["DELETE"])
def delete_sweet(sweet_id):
    return delete_sweets(sweet_id)