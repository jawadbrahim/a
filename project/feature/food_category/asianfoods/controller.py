from flask import Response, request, json, jsonify
from project.model.asianfoods import Asianfood
from database.postgres import db
from project.feature.food_category.asianfoods.schema import AsianfoodSchema
from project.cache.redis_cache import get_cached_data, set_cached_data
from .decorators import validate_asianfood_existence

asianfood_schema = AsianfoodSchema()
asianfoods_schema = AsianfoodSchema(many=True)

def create_asianfood():
    if request.method == "POST":
        asianfood_data = asianfood_schema.load(request.json)
        new_asianfood = Asianfood(**asianfood_data)
        db.session.add(new_asianfood)
        db.session.commit()

        cache_key = f'asianfood:{new_asianfood.id}'
        set_cached_data(cache_key, "", expiration_time=3600)

        response_data = {
            "message": "Created successfully",
            "food_categories": None 
        }
        json_data = json.dumps(response_data, ensure_ascii=False)
        response = Response(json_data, content_type='application/json; charset=utf-8')
        return response, 201

def get_asianfoods_list():
    asianfoods_list = Asianfood.query.all()
    asianfoods = []

    for asianfood in asianfoods_list:
        asianfoods.append({
            "title": asianfood.title,
            "description": asianfood.description,
            "picture": asianfood.picture,
            "ingredients": asianfood.ingredients,
        })

    response_data = { "food_categories": {"asianfoods":asianfoods} } 
    json_data = json.dumps(response_data, ensure_ascii=False)
    response = Response(json_data, content_type='application/json; charset=utf-8')
    return response

def update_asianfoods(asianfood_id):
    asianfood_data = asianfood_schema.load(request.json)

    asianfood = Asianfood.query.get(asianfood_id)

    asianfood.title = asianfood_data["title"]
    asianfood.description = asianfood_data.get("description")
    asianfood.picture = asianfood_data.get("picture")
    asianfood.ingredients = asianfood_data.get("ingredients")

    db.session.commit()

    cache_key = f'asianfood:{asianfood_id}'
    set_cached_data(cache_key, "", expiration_time=3600)

    response_data = {
        "message": "Update successfully",
        "food_categories": None  
    }
    json_data = json.dumps(response_data, ensure_ascii=False)
    response = Response(json_data, content_type='application/json; charset=utf-8')
    return response, 200

@validate_asianfood_existence
def get_asianfood_single(asianfood_id):
    cache_key = f'asianfood:{asianfood_id}'
    cached_data = get_cached_data(cache_key)

    if cached_data:
        response = Response(cached_data, content_type='application/json; charset=utf-8')
        return response

    asianfood = Asianfood.query.get(asianfood_id)

    if asianfood:
        response_data = asianfood_schema.dump(asianfood)

        set_cached_data(cache_key, response_data)

        json_data = json.dumps(response_data, ensure_ascii=False)
        response = Response(json_data, content_type='application/json; charset=utf-8')
        return response
    else:
        response_data = { "food_categories": {"error": "Asianfood not found"}}  # Change "meta" to "food_categories"
        json_data = json.dumps(response_data, ensure_ascii=False)
        response = Response(json_data, content_type='application/json; charset=utf-8')
        return response, 404

def delete_asianfoods(asianfood_id):
    asianfood = Asianfood.query.get(asianfood_id)
    if asianfood:
        db.session.delete(asianfood)
        db.session.commit()

        cache_key = f'asianfood:{asianfood_id}'
        set_cached_data(cache_key, "", expiration_time=3600)

        response_data = {
            "message": "Delete successfully",
            "food_categories": None  
        }
        json_data = json.dumps(response_data, ensure_ascii=False)
        response = Response(json_data, content_type='application/json; charset=utf-8')
        return response, 200
