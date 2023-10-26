from flask import Blueprint
from project.feature.sauces.controller import add_get_sauces,update_sauces,get_sauces,delete_sauces
from .error_handler import handle_sauce_exceptions

sauces_bp=Blueprint("sauces",__name__,url_prefix="/sauces")
handle_sauce_exceptions(sauces_bp)
@sauces_bp.route("/", methods=["POST", "GET"])
def sauces():
    return add_get_sauces()

@sauces_bp.route("/<int:sauce_id>", methods=["PUT"])
def put_sauce(sauce_id):
    return update_sauces(sauce_id)

@sauces_bp.route("/<int:sauce_id>", methods=["GET"])
def get_sauce(sauce_id):
    return get_sauces(sauce_id)

@sauces_bp.route("/<int:sauce_id>", methods=["DELETE"])
def delete_sauce(sauce_id):
    return delete_sauces(sauce_id)