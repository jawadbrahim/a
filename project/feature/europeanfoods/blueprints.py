from flask import Blueprint
from project.feature.europeanfoods.controller import add_get_europeanfoods,get_europeanfoods,update_europeanfoods,delete_europeanfoods
from .error_handler import handle_europeanfood_exceptions


europeanfoods_bp=Blueprint("europeanfoods",__name__,url_prefix="/europeanfoods")
handle_europeanfood_exceptions(europeanfoods_bp)
@europeanfoods_bp.route("/", methods=["POST", "GET"])
def europeanfood():
    return add_get_europeanfoods()


@europeanfoods_bp.route("/<int:europeanfood_id>", methods=["PUT"])
def put_europeanfood(europeanfood_id):
    return update_europeanfoods(europeanfood_id)

@europeanfoods_bp.route("/<int:europeanfood_id>", methods=["GET"])
def get_europeanfood(europeanfood_id):
    return get_europeanfoods(europeanfood_id)

@europeanfoods_bp.route("/<int:europeanfood_id>", methods=["DELETE"])
def delete_europeanfood(europeanfood_id):
    return delete_europeanfoods(europeanfood_id)