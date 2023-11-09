from flask import Blueprint, request
from project.feature.food_category.salades.controller import create_salade, get_salades_list, update_salades, delete_salades, get_salade_single
from .error_handler import handle_salade_exceptions

salades_bp = Blueprint("salades", __name__, url_prefix="/salades")

handle_salade_exceptions(salades_bp)

@salades_bp.route("/", methods=["POST", "GET"])
def salades():
    if request.method == "POST":
        return create_salade()
    elif request.method == "GET":
        return get_salades_list()

@salades_bp.route("/<int:salade_id>", methods=["PUT"])
def update_salade(salade_id):
    return update_salades(salade_id)

@salades_bp.route("/<int:salade_id>", methods=["GET"])
def get_salade(salade_id):
    return get_salade_single(salade_id)

@salades_bp.route("/<int:salade_id>", methods=["DELETE"])
def delete_salade(salade_id):
    return delete_salades(salade_id)
