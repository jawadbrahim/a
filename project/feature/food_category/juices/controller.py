from flask import Response, request, json
from project.model.juices import Juice
from database.postgres import db
from project.feature.food_category.juices.schema import JuiceSchema
from project.cache.redis_cache import get_cached_data, set_cached_data
from .decorators import validate_juice_existence

juice_schema = JuiceSchema()
juices_schema = JuiceSchema(many=True)

def create_juice():
    if request.method == "POST":
        juice_data = juice_schema.load(request.json)
        new_juice = Juice(**juice_data)
        db.session.add(new_juice)
        db.session.commit()

        cache_key = f'juice:{new_juice.id}'
        set_cached_data(cache_key, "", expiration_time=3600)

        response_data = {
            "message": "Created successfully",
            "food_categories": None  
        }
        json_data = json.dumps(response_data, ensure_ascii=False)
        response = Response(json_data, content_type='application/json; charset=utf-8')
        return response, 201

def get_juices_list():
    juices_list = Juice.query.all()
    juices = []

    for juice in juices_list:
        juices.append({
            "title": juice.title,
            "description": juice.description,
            "picture": juice.picture,
            "ingredients": juice.ingredients,
        })

    response_data = { "food_categories": {"juices":juices}} 
    json_data = json.dumps(response_data, ensure_ascii=False)
    response = Response(json_data, content_type='application/json; charset=utf-8')
    return response

def update_juices(juice_id):
    juice_data = juice_schema.load(request.json)

    juice = Juice.query.get(juice_id)

    juice.title = juice_data["title"]
    juice.description = juice_data.get("description")
    juice.picture = juice_data.get("picture")
    juice.ingredients = juice_data.get("ingredients")

    db.session.commit()

    cache_key = f'juice:{juice_id}'
    set_cached_data(cache_key, "", expiration_time=3600)

    response_data = {
        "message": "Update successfully",
        "food_categories": None  
    }
    json_data = json.dumps(response_data, ensure_ascii=False)
    response = Response(json_data, content_type='application/json; charset=utf-8')
    return response, 200

@validate_juice_existence
def get_juice_single(juice_id):
    cache_key = f'juice:{juice_id}'
    cached_data = get_cached_data(cache_key)

    if cached_data:
        response = Response(cached_data, content_type='application/json; charset=utf-8')
        return response

    juice = Juice.query.get(juice_id)

    if juice:
        response_data = juice_schema.dump(juice)

        set_cached_data(cache_key, response_data)

        json_data = json.dumps(response_data, ensure_ascii=False)
        response = Response(json_data, content_type='application/json; charset=utf-8')
        return response
    else:
        response_data = {"food_categories": {"error": "Juice not found"}}  
        json_data = json.dumps(response_data, ensure_ascii=False)
        response = Response(json_data, content_type='application/json; charset=utf-8')
        return response, 404

def delete_juices(juice_id):
    juice = Juice.query.get(juice_id)
    if juice:
        db.session.delete(juice)
        db.session.commit()

        cache_key = f'juice:{juice_id}'
        set_cached_data(cache_key, "", expiration_time=3600)

        response_data = {
            "message": "Delete successfully",
            "food_categories": None  
        }
        json_data = json.dumps(response_data, ensure_ascii=False)
        response = Response(json_data, content_type='application/json; charset=utf-8')
        return response, 200
