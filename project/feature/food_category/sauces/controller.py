from flask import Response, request, json, jsonify
from project.model.sauces import Sauce
from database.postgres import db
from project.feature.food_category.sauces.schema import SauceSchema
from project.cache.redis_cache import get_cached_data, set_cached_data
from .decorators import validate_sauce_existence

sauce_schema = SauceSchema()
sauces_schema = SauceSchema(many=True)

def create_sauce():
    if request.method == "POST":
        sauce_data = sauce_schema.load(request.json)
        new_sauce = Sauce(**sauce_data)
        db.session.add(new_sauce)
        db.session.commit()

        cache_key = f'sauce:{new_sauce.id}'
        set_cached_data(cache_key, "", expiration_time=3600)

        response_data = {
            "message": "Created successfully",
            "food_categories": None  
        }
        json_data = json.dumps(response_data, ensure_ascii=False)
        response = Response(json_data, content_type='application/json; charset=utf-8')
        return response, 201

def get_sauces_list():
    sauces_list = Sauce.query.all()
    sauces = []

    for sauce in sauces_list:
        sauces.append({
            "title": sauce.title,
            "description": sauce.description,
            "picture": sauce.picture,
            "ingredients": sauce.ingredients,
        })

    response_data = { "food_categories": {"sauces":sauces}}  
    json_data = json.dumps(response_data, ensure_ascii=False)
    response = Response(json_data, content_type='application/json; charset=utf-8')
    return response

def update_sauces(sauce_id):
    sauce_data = sauce_schema.load(request.json)

    sauce = Sauce.query.get(sauce_id)

    sauce.title = sauce_data["title"]
    sauce.description = sauce_data.get("description")
    sauce.picture = sauce_data.get("picture")
    sauce.ingredients = sauce_data.get("ingredients")

    db.session.commit()

    cache_key = f'sauce:{sauce_id}'
    set_cached_data(cache_key, "", expiration_time=3600)

    response_data = {
        "message": "Update successfully",
        "food_categories": None  
    }
    json_data = json.dumps(response_data, ensure_ascii=False)
    response = Response(json_data, content_type='application/json; charset=utf-8')
    return response, 200

@validate_sauce_existence
def get_sauce_single(sauce_id):
    cache_key = f'sauce:{sauce_id}'
    cached_data = get_cached_data(cache_key)

    if cached_data:
        response = Response(cached_data, content_type='application/json; charset=utf-8')
        return response

    sauce = Sauce.query.get(sauce_id)

    if sauce:
        response_data = sauce_schema.dump(sauce)

        set_cached_data(cache_key, response_data)

        json_data = json.dumps(response_data, ensure_ascii=False)
        response = Response(json_data, content_type='application/json; charset=utf-8')
        return response
    else:
        response_data = {"food_categories": {"error": "Sauce not found"}}  
        json_data = json.dumps(response_data, ensure_ascii=False)
        response = Response(json_data, content_type='application/json; charset=utf-8')
        return response, 404

def delete_sauces(sauce_id):
    sauce = Sauce.query.get(sauce_id)
    if sauce:
        db.session.delete(sauce)
        db.session.commit()

        cache_key = f'sauce:{sauce_id}'
        set_cached_data(cache_key, "", expiration_time=3600)

        response_data = {
            "message": "Delete successfully",
            "food_categories": None  
        }
        json_data = json.dumps(response_data, ensure_ascii=False)
        response = Response(json_data, content_type='application/json; charset=utf-8')
        return response, 200
