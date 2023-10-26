from flask import Blueprint
from project.feature.icecreams.controller import add_get_icecreams,get_icecreams,delete_icecreams,update_icecreams
from .error_handler import handle_icecream_exceptions

icecreams_bp=Blueprint("icecreams",__name__,url_prefix="/icecreams")
handle_icecream_exceptions(icecreams_bp)


@icecreams_bp.route("/", methods=["POST", "GET"])
def icecreams():
    return add_get_icecreams()

@icecreams_bp.route("/<int:icecream_id>", methods=["PUT"])
def put_icecream(icecream_id):
    return update_icecreams(icecream_id)

@icecreams_bp.route("/<int:icecream_id>", methods=["GET"])
def get_icecream(icecream_id):
    return get_icecreams(icecream_id)

@icecreams_bp.route("/<int:icecream_id>", methods=["DELETE"])
def delete_icecream(icecream_id):
    return delete_icecreams(icecream_id)