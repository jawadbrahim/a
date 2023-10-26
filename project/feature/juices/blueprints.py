from flask import Blueprint
from .error_handler import handle_juice_exceptions
from project.feature.juices.controller import add_get_juices,update_juices,get_juices,delete_juices


juices_bp=Blueprint("juices",__name__,url_prefix="/juices")
handle_juice_exceptions(juices_bp)

@juices_bp.route("/", methods=["POST", "GET"])
def juices():
    return add_get_juices()

@juices_bp.route("/<int:juice_id>", methods=["PUT"])
def put_juice(juice_id):
    return update_juices(juice_id)

@juices_bp.route("/<int:juice_id>", methods=["GET"])
def get_juice(juice_id):
    return get_juices(juice_id)

@juices_bp.route("/<int:juice_id>", methods=["DELETE"])
def delete_juice(juice_id):
    return delete_juices(juice_id)