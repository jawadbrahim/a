from flask import Response, request, json
from project.model.icecreams import Icecream
from database.postgres import db
from project.feature.food_category.icecreams.schema import IcecreamSchema
from project.cache.redis_cache import get_cached_data, set_cached_data
from .decorators import validate_icecream_existence

icecream_schema = IcecreamSchema()
icecreams_schema = IcecreamSchema(many=True)

def create_icecream():
    if request.method == "POST":
        icecream_data = icecream_schema.load(request.json)
        new_icecream = Icecream(**icecream_data)
        db.session.add(new_icecream)
        db.session.commit()

        cache_key = f'icecream:{new_icecream.id}'
        set_cached_data(cache_key, "", expiration_time=3600)

        response_data = {
            "message": "Created successfully",
            "food_categories": None 
        }
        json_data = json.dumps(response_data, ensure_ascii=False)
        response = Response(json_data, content_type='application/json; charset=utf-8')
        return response, 201

def get_icecreams_list():
    icecreams_list = Icecream.query.all()
    icecreams = []

    for icecream in icecreams_list:
        icecreams.append({
            "title": icecream.title,
            "description": icecream.description,
            "picture": icecream.picture,
            "ingredients": icecream.ingredients,
        })

    response_data = { "food_categories": {"icecreams":icecreams} } 
    json_data = json.dumps(response_data, ensure_ascii=False)
    response = Response(json_data, content_type='application/json; charset=utf-8')
    return response

def update_icecreams(icecream_id):
    icecream_data = icecream_schema.load(request.json)

    icecream = Icecream.query.get(icecream_id)

    icecream.title = icecream_data["title"]
    icecream.description = icecream_data.get("description")
    icecream.picture = icecream_data.get("picture")
    icecream.ingredients = icecream_data.get("ingredients")

    db.session.commit()

    cache_key = f'icecream:{icecream_id}'
    set_cached_data(cache_key, "", expiration_time=3600)

    response_data = {
        "message": "Update successfully",
        "food_categories": None 
    }
    json_data = json.dumps(response_data, ensure_ascii=False)
    response = Response(json_data, content_type='application/json; charset=utf-8')
    return response, 200

@validate_icecream_existence
def get_icecream_single(icecream_id):
    cache_key = f'icecream:{icecream_id}'
    cached_data = get_cached_data(cache_key)

    if cached_data:
        response = Response(cached_data, content_type='application/json; charset=utf-8')
        return response

    icecream = Icecream.query.get(icecream_id)

    if icecream:
        response_data = icecream_schema.dump(icecream)

        set_cached_data(cache_key, response_data)

        json_data = json.dumps(response_data, ensure_ascii=False)
        response = Response(json_data, content_type='application/json; charset=utf-8')
        return response
    else:
        response_data = { "food_categories": {"error": "Icecream not found"}}  
        json_data = json.dumps(response_data, ensure_ascii=False)
        response = Response(json_data, content_type='application/json; charset=utf-8')
        return response, 404

def delete_icecreams(icecream_id):
    icecream = Icecream.query.get(icecream_id)
    if icecream:
        db.session.delete(icecream)
        db.session.commit()

        cache_key = f'icecream:{icecream_id}'
        set_cached_data(cache_key, "", expiration_time=3600)

        response_data = {
            "message": "Delete successfully",
            "food_categories": None  
        }
        json_data = json.dumps(response_data, ensure_ascii=False)
        response = Response(json_data, content_type='application/json; charset=utf-8')
        return response, 200
