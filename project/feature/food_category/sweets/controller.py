from flask import Response, request, json, jsonify
from project.model.sweets import Sweet
from database.postgres import db
from project.feature.food_category.sweets.schema import SweetSchema
from project.cache.redis_cache import get_cached_data, set_cached_data
from .decorators import validate_sweet_existence

sweet_schema = SweetSchema()
sweets_schema = SweetSchema(many=True)

def create_sweet():
    if request.method == "POST":
        sweet_data = sweet_schema.load(request.json)
        new_sweet = Sweet(**sweet_data)
        db.session.add(new_sweet)
        db.session.commit()

        cache_key = f'sweet:{new_sweet.id}'
        set_cached_data(cache_key, "", expiration_time=3600)

        response_data = {
            "message": "Created successfully",
            "food_categories": None  
        }
        json_data = json.dumps(response_data, ensure_ascii=False)
        response = Response(json_data, content_type='application/json; charset=utf-8')
        return response, 201

def get_sweets_list():
    sweets_list = Sweet.query.all()
    sweets = []

    for sweet in sweets_list:
        sweets.append({
            "title": sweet.title,
            "description": sweet.description,
            "picture": sweet.picture,
            "ingredients": sweet.ingredients,
        })

    response_data = { "food_categories": {"sweets":sweets}}  
    json_data = json.dumps(response_data, ensure_ascii=False)
    response = Response(json_data, content_type='application/json; charset=utf-8')
    return response

def update_sweets(sweet_id):
    sweet_data = sweet_schema.load(request.json)

    sweet = Sweet.query.get(sweet_id)

    sweet.title = sweet_data["title"]
    sweet.description = sweet_data.get("description")
    sweet.picture = sweet_data.get("picture")
    sweet.ingredients = sweet_data.get("ingredients")

    db.session.commit()

    cache_key = f'sweet:{sweet_id}'
    set_cached_data(cache_key, "", expiration_time=3600)

    response_data = {
        "message": "Update successfully",
        "food_categories": None  
    }
    json_data = json.dumps(response_data, ensure_ascii=False)
    response = Response(json_data, content_type='application/json; charset=utf-8')
    return response, 200

@validate_sweet_existence
def get_sweet_single(sweet_id):
    cache_key = f'sweet:{sweet_id}'
    cached_data = get_cached_data(cache_key)

    if cached_data:
        response = Response(cached_data, content_type='application/json; charset=utf-8')
        return response

    sweet = Sweet.query.get(sweet_id)

    if sweet:
        response_data = sweet_schema.dump(sweet)

        set_cached_data(cache_key, response_data)

        json_data = json.dumps(response_data, ensure_ascii=False)
        response = Response(json_data, content_type='application/json; charset=utf-8')
        return response
    else:
        response_data = { "food_categories": {"error": "Sweet not found"}}  
        json_data = json.dumps(response_data, ensure_ascii=False)
        response = Response(json_data, content_type='application/json; charset=utf-8')
        return response, 404

def delete_sweets(sweet_id):
    sweet = Sweet.query.get(sweet_id)

    if sweet:
        db.session.delete(sweet)
        db.session.commit()

        cache_key = f'sweet:{sweet_id}'
        set_cached_data(cache_key, "", expiration_time=3600)

        response_data = {
            "message": "Delete successfully",
            "food_categories": None  
        }
        json_data = json.dumps(response_data, ensure_ascii=False)
        response = Response(json_data, content_type='application/json; charset=utf-8')
        return response, 200
