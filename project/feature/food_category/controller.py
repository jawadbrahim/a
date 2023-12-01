from flask import jsonify, request, json, Response
from project.model.Food import Food, Categories
from database.postgres import db
from .pydantic_models import FoodPydantic
from .messages import FAILED_TO_CREATE_FOOD, FOOD_NOT_FOUND,UPDATE_SUCCESSFULLY, CREATED_SUCCESSFULLY, DELETE_SUCCESSFULLY
from .decorators import validate_properties_existence
from pydantic import ValidationError
from .combine import PydanticToDataclassConverter, DataclassToPydanticConverter

@validate_properties_existence
def create_foods():
    if request.method == "POST":
        try:
            data = request.json

            
            food_data_pydantic = FoodPydantic(**data)

            
            food_data_dataclass = PydanticToDataclassConverter.food_pydantic_to_dataclass(food_data_pydantic)

            
            category_data = food_data_pydantic.category.dict() if food_data_pydantic.category else {"title": None}
            category_name = category_data.get("title", "")
            
            
            category = db.session.query(Categories).filter_by(title=category_name).first()

            
            new_food = Food(
                title=food_data_dataclass.title,
                description=food_data_pydantic.description,
                picture=food_data_pydantic.picture,
                ingredients=food_data_pydantic.ingredients,
            )

            
            if category:
                new_food.category = category
            else:
                new_category = Categories(title=category_name)
                new_food.category = new_category

            
            db.session.add(new_food)
            db.session.commit()

            return jsonify(CREATED_SUCCESSFULLY)

        except ValidationError as e:
            return jsonify(FAILED_TO_CREATE_FOOD)

        except Exception as e:
            return jsonify( FAILED_TO_CREATE_FOOD)

    return jsonify(CREATED_SUCCESSFULLY)
def get_foods_list():
    offset = request.args.get("offset", type=int, default=0)
    limit = request.args.get("limit", type=int, default=50)

   
    foods = db.session.query(Food).limit(limit).offset(offset).all()
    

    
    foods_data = []

    for food in foods:
        food_data = {
            "id": food.id,
            "title": food.title,
            "description": food.description,
            "picture": food.picture,
            "ingredients": food.ingredients,
        }

        category = food.category

        if category:
            food_data["category"] = {
                "id": category.id,
                "title": category.title,
            }

        foods_data.append(food_data)

    response_data = {"foods": foods_data}
    response = json.dumps(response_data, ensure_ascii=False)

    return Response(response, content_type="application/json;")

def update_foods(food_id):
    data = request.json
    foods_title = data["title"]
    foods_description = data.get("description")
    foods_picture = data.get("picture")
    foods_ingredients = data.get("ingredients")
    category_id = data.get("category_id")

    food = db.session.query(Food).get(food_id)

    if not food:
        return jsonify(FOOD_NOT_FOUND)

    category = db.session.query(Categories).get(category_id) if category_id else None

    food.title = foods_title
    food.description = foods_description
    food.picture = foods_picture
    food.ingredients = foods_ingredients

    food.category = category

    db.session.commit()

    return jsonify(UPDATE_SUCCESSFULLY)


def get_foods_single(food_id):
    food = db.session.query(Food).get(food_id)

    if food:
        food_data = {
            "id": food.id,
            "title": food.title,
            "description": food.description,
            "picture": food.picture,
            "ingredients": food.ingredients,
        }

        category = food.category

        if category:
            food_data["category"] = {
                "id": category.id,
                "title": category.title,
            }

        return jsonify(food_data)
    else:
        return jsonify(FOOD_NOT_FOUND)

def delete_foods(food_id):
    food = db.session.query(Food).get(food_id)
    if food:
        db.session.delete(food)
        db.session.commit()
        return jsonify(DELETE_SUCCESSFULLY)
    else:
        return jsonify(FOOD_NOT_FOUND)
