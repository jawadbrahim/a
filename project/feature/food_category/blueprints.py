from flask import Blueprint
from project.feature.food_category.controller import create_foods,get_foods_list,get_foods_single,delete_foods,update_foods


foods_bp = Blueprint("foods", __name__, url_prefix="/foods")



@foods_bp.route("/", methods=["POST"], strict_slashes=False)
def create_food_endpoint():
    return create_foods()

@foods_bp.route("/", methods=["GET"])
def get_foods_list_endpoint():
    return get_foods_list()

@foods_bp.route("/<int:food_id>", methods=["PUT"])
def update_food(food_id):
    return update_foods(food_id)

@foods_bp.route("/<int:food_id>", methods=["GET"])
def get_food(food_id):
    return get_foods_single(food_id)

@foods_bp.route("/<int:food_id>", methods=["DELETE"])
def delete_food(food_id):
    return delete_foods(food_id)