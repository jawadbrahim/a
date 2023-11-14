from flask import jsonify, request, json, Response
from project.model.Food import Food, Categories
from database.postgres import db
from project.feature.food_category.schema import FoodSchema
from .messages import FAILED_TO_CREATE_FOOD, FOOD_NOT_FOUND,UPDATE_SUCCESSFULLY, CREATED_SUCCESSFULLY, DELETE_SUCCESSFULLY
from .decorators import validate_properties_existence
food_schema = FoodSchema()
foods_schema = FoodSchema(many=True)



@validate_properties_existence
def create_foods():
    if request.method == "POST":
        try:
           
            data = food_schema.load(request.json)
        except Exception as e:
            return jsonify(FAILED_TO_CREATE_FOOD)
        
        food_id = data.get("id")
        foods_title = data.get("title")
        foods_description = data.get("description")
        foods_picture = data.get("picture")
        foods_ingredients = data.get("ingredients")

        if food_id:
           
            existing_food = Food.query.get(food_id)

            if existing_food:
                existing_food.title = foods_title
                existing_food.description = foods_description
                existing_food.picture = foods_picture
                existing_food.ingredients = foods_ingredients
            else:
                return jsonify(FAILED_TO_CREATE_FOOD)

        else:
            
            category_data = data.get("category", {})
            category_name = category_data.get("title", "") 
            category = db.session.query(Categories).filter_by(title=category_name).first()

            new_food = Food(
                title=foods_title,
                description=foods_description,
                picture=foods_picture,
                ingredients=foods_ingredients,
            )

            if category:
                new_food.category = category
            else:
               
                new_category = Categories(title=category_name)
                new_food.category = new_category

            db.session.add(new_food)
            db.session.commit()

            
            serialized_data = food_schema.dump(new_food)
            return jsonify(serialized_data, CREATED_SUCCESSFULLY)

    
    foods_list = Food.query.all()
    serialized_foods = foods_schema.dump(foods_list)
    return jsonify(serialized_foods,CREATED_SUCCESSFULLY)

def get_foods_list():
    offset = request.args.get("offset", type=int, default=0)
    limit = request.args.get("limit", type=int, default=20)

   
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
    foods_title = request.json["title"]
    foods_description = request.json.get("description")
    foods_picture = request.json.get("picture")
    foods_ingredients = request.json.get("ingredients")
    category_id = request.json.get("category_id")

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
