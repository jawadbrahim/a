from flask import Response, request, json
from project.model.europeanfoods import Europeanfood
from database.postgres import db
from project.feature.food_category.europeanfoods.schema import EuropeanfoodSchema
from project.cache.redis_cache import get_cached_data, set_cached_data
from .decorators import validate_europeanfood_existence

europeanfood_schema = EuropeanfoodSchema()
europeanfoods_schema = EuropeanfoodSchema(many=True)

def create_europeanfood():
    if request.method == "POST":
        europeanfood_data = europeanfood_schema.load(request.json)
        new_europeanfood = Europeanfood(**europeanfood_data)
        db.session.add(new_europeanfood)
        db.session.commit()

        cache_key = f'europeanfood:{new_europeanfood.id}'
        set_cached_data(cache_key, "", expiration_time=3600)

        response_data = {
            "message": "Created successfully",
            "food_categories": None 
        }
        json_data = json.dumps(response_data, ensure_ascii=False)
        response = Response(json_data, content_type='application/json; charset=utf-8')
        return response, 201

def get_europeanfoods_list():
    europeanfoods_list = Europeanfood.query.all()
    europeanfoods = []

    for europeanfood in europeanfoods_list:
        europeanfoods.append({
            "title": europeanfood.title,
            "description": europeanfood.description,
            "picture": europeanfood.picture,
            "ingredients": europeanfood.ingredients,
        })

    response_data = {"message": None, "food_categories": {"europeanfoods":europeanfoods}}  # Change "meta" to "food_categories
    json_data = json.dumps(response_data, ensure_ascii=False)
    response = Response(json_data, content_type='application/json; charset=utf-8')
    return response

def update_europeanfoods(europeanfood_id):
    europeanfood_data = europeanfood_schema.load(request.json)

    europeanfood = Europeanfood.query.get(europeanfood_id)

    europeanfood.title = europeanfood_data["title"]
    europeanfood.description = europeanfood_data.get("description")
    europeanfood.picture = europeanfood_data.get("picture")
    europeanfood.ingredients = europeanfood_data.get("ingredients")

    db.session.commit()

    cache_key = f'europeanfood:{europeanfood_id}'
    set_cached_data(cache_key, "", expiration_time=3600)

    response_data = {
        "message": "Update successfully",
        "food_categories": None  
    }
    json_data = json.dumps(response_data, ensure_ascii=False)
    response = Response(json_data, content_type='application/json; charset=utf-8')
    return response, 200

@validate_europeanfood_existence
def get_europeanfood_single(europeanfood_id):
    cache_key = f'europeanfood:{europeanfood_id}'
    cached_data = get_cached_data(cache_key)

    if cached_data:
        response = Response(cached_data, content_type='application/json; charset=utf-8')
        return response

    europeanfood = Europeanfood.query.get(europeanfood_id)

    if europeanfood:
        response_data = europeanfood_schema.dump(europeanfood)

        set_cached_data(cache_key, response_data)

        json_data = json.dumps(response_data, ensure_ascii=False)
        response = Response(json_data, content_type='application/json; charset=utf-8')
        return response
    else:
        response_data = {"food_categories": {"error": "Europeanfood not found"}}  
        json_data = json.dumps(response_data, ensure_ascii=False)
        response = Response(json_data, content_type='application/json; charset=utf-8')
        return response, 404

def delete_europeanfoods(europeanfood_id):
    europeanfood = Europeanfood.query.get(europeanfood_id)
    if europeanfood:
        db.session.delete(europeanfood)
        db.session.commit()

        cache_key = f'europeanfood:{europeanfood_id}'
        set_cached_data(cache_key, "", expiration_time=3600)

        response_data = {
            "message": "Delete successfully",
            "food_categories": None  
        }
        json_data = json.dumps(response_data, ensure_ascii=False)
        response = Response(json_data, content_type='application/json; charset=utf-8')
        return response, 200
