from flask import Blueprint
from .error_handler import handle_salade_exceptions
from project.feature.salades.controller import add_get_salades,update_salades,get_salades,delete_salades


salades_bp=Blueprint("salades",__name__,url_prefix="/salades")
handle_salade_exceptions(salades_bp)
@salades_bp.route("/", methods=["POST", "GET"])
def salades():
    return add_get_salades()

@salades_bp.route("/<int:salade_id>", methods=["PUT"])
def put_salade(salade_id):
    return update_salades(salade_id)

@salades_bp.route("/<int:salade_id>", methods=["GET"])
def get_salade(salade_id):
    return get_salades(salade_id)

@salades_bp.route("/<int:salade_id>", methods=["DELETE"])
def delete_salade(salade_id):
    return delete_salades(salade_id)