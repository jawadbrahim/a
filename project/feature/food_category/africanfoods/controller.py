from flask import Response, request, json, jsonify
from project.model.africanfoods import Africanfood
from database.postgres import db
from project.feature.food_category.africanfoods.schema import AfricanfoodSchema
from project.cache.redis_cache import get_cached_data, set_cached_data
from .decorators import validate_africanfood_existence

africanfood_schema = AfricanfoodSchema()
africanfoods_schema = AfricanfoodSchema(many=True)

def create_africanfood():
    if request.method == "POST":
        africanfood_data = africanfood_schema.load(request.json)
        new_africanfood = Africanfood(**africanfood_data)
        db.session.add(new_africanfood)
        db.session.commit()

        cache_key = f'africanfood:{new_africanfood.id}'
        set_cached_data(cache_key, "", expiration_time=3600)

        response_data = {
            "message": "Created successfully",
            "food_categories": None  
        }
        json_data = json.dumps(response_data, ensure_ascii=False)
        response = Response(json_data, content_type='application/json; charset=utf-8')
        return response, 201

def get_africanfoods_list():
    africanfoods_list = Africanfood.query.all()
    africanfoods = []

    for africanfood in africanfoods_list:
        africanfoods.append({
            "title": africanfood.title,
            "description": africanfood.description,
            "picture": africanfood.picture,
            "ingredients": africanfood.ingredients,
        })

    response_data = { "food_categories": {"africanfoods":africanfoods}}  
    json_data = json.dumps(response_data, ensure_ascii=False)
    response = Response(json_data, content_type='application/json; charset=utf-8')
    return response

def update_africanfoods(africanfood_id):
    africanfood_data = africanfood_schema.load(request.json)

    africanfood = Africanfood.query.get(africanfood_id)

    africanfood.title = africanfood_data["title"]
    africanfood.description = africanfood_data.get("description")
    africanfood.picture = africanfood_data.get("picture")
    africanfood.ingredients = africanfood_data.get("ingredients")

    db.session.commit()

    cache_key = f'africanfood:{africanfood_id}'
    set_cached_data(cache_key, "", expiration_time=3600)

    response_data = {
        "message": "Update successfully",
        "food_categories": None  
    }
    json_data = json.dumps(response_data, ensure_ascii=False)
    response = Response(json_data, content_type='application/json; charset=utf-8')
    return response, 200

@validate_africanfood_existence
def get_africanfood_single(africanfood_id):
    cache_key = f'africanfood:{africanfood_id}'
    cached_data = get_cached_data(cache_key)

    if cached_data:
        response = Response(cached_data, content_type='application/json; charset=utf-8')
        return response

    africanfood = Africanfood.query.get(africanfood_id)

    if africanfood:
        response_data = africanfood_schema.dump(africanfood)

        set_cached_data(cache_key, response_data)

        json_data = json.dumps(response_data, ensure_ascii=False)
        response = Response(json_data, content_type='application/json; charset=utf-8')
        return response
    else:
        response_data = { "food_categories": {"error": "Africanfood not found"}}  
        json_data = json.dumps(response_data, ensure_ascii=False)
        response = Response(json_data, content_type='application/json; charset=utf-8')
        return response, 404

def delete_africanfoods(africanfood_id):
    africanfood = Africanfood.query.get(africanfood_id)
    if africanfood:
        db.session.delete(africanfood)
        db.session.commit()

        cache_key = f'africanfood:{africanfood_id}'
        set_cached_data(cache_key, "", expiration_time=3600)

        response_data = {
            "message": "Delete successfully",
            "food_categories": None  
        }
        json_data = json.dumps(response_data, ensure_ascii=False)
        response = Response(json_data, content_type='application/json; charset=utf-8')
        return response, 200
