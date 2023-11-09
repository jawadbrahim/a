from flask import Response, request, json
from project.model.americanfoods import Americanfood
from database.postgres import db
from project.feature.food_category.americanfoods.schema import AmericanfoodSchema
from project.cache.redis_cache import get_cached_data, set_cached_data
from .decorators import validate_americanfood_existence

americanfood_schema = AmericanfoodSchema()
americanfoods_schema = AmericanfoodSchema(many=True)

def create_americanfood():
    if request.method == "POST":
        americanfood_data = americanfood_schema.load(request.json)
        new_americanfood = Americanfood(**americanfood_data)
        db.session.add(new_americanfood)
        db.session.commit()

        cache_key = f'americanfood:{new_americanfood.id}'
        set_cached_data(cache_key, "", expiration_time=3600)

        response_data = {
            "message": "Created successfully",
            "food_categories": None  
        }
        json_data = json.dumps(response_data, ensure_ascii=False)
        response = Response(json_data, content_type='application/json; charset=utf-8')
        return response, 201

def get_americanfoods_list():
    americanfoods_list = Americanfood.query.all()
    americanfoods = []

    for americanfood in americanfoods_list:
        americanfoods.append({
            "title": americanfood.title,
            "description": americanfood.description,
            "picture": americanfood.picture,
            "ingredients": americanfood.ingredients,
        })

    response_data = {"food_categories": {"americanfoods":americanfoods}}  
    json_data = json.dumps(response_data, ensure_ascii=False)
    response = Response(json_data, content_type='application/json; charset=utf-8')
    return response

def update_americanfoods(americanfood_id):
    americanfood_data = americanfood_schema.load(request.json)

    americanfood = Americanfood.query.get(americanfood_id)

    americanfood.title = americanfood_data["title"]
    americanfood.description = americanfood_data.get("description")
    americanfood.picture = americanfood_data.get("picture")
    americanfood.ingredients = americanfood_data.get("ingredients")

    db.session.commit()

    cache_key = f'americanfood:{americanfood_id}'
    set_cached_data(cache_key, "", expiration_time=3600)

    response_data = {
        "message": "Update successfully",
        "food_categories": None  
    }
    json_data = json.dumps(response_data, ensure_ascii=False)
    response = Response(json_data, content_type='application/json; charset=utf-8')
    return response, 200

@validate_americanfood_existence
def get_americanfood_single(americanfood_id):
    cache_key = f'americanfood:{americanfood_id}'
    cached_data = get_cached_data(cache_key)

    if cached_data:
        response = Response(cached_data, content_type='application/json; charset=utf-8')
        return response

    americanfood = Americanfood.query.get(americanfood_id)

    if americanfood:
        response_data = americanfood_schema.dump(americanfood)

        set_cached_data(cache_key, response_data)

        json_data = json.dumps(response_data, ensure_ascii=False)
        response = Response(json_data, content_type='application/json; charset=utf-8')
        return response
    else:
        response_data = { "food_categories": {"error": "Americanfood not found"}}  
        json_data = json.dumps(response_data, ensure_ascii=False)
        response = Response(json_data, content_type='application/json; charset=utf-8')
        return response, 404

def delete_americanfoods(americanfood_id):
    americanfood = Americanfood.query.get(americanfood_id)
    if americanfood:
        db.session.delete(americanfood)
        db.session.commit()

        cache_key = f'americanfood:{americanfood_id}'
        set_cached_data(cache_key, "", expiration_time=3600)

        response_data = {
            "message": "Delete successfully",
            "food_categories": None  
        }
        json_data = json.dumps(response_data, ensure_ascii=False)
        response = Response(json_data, content_type='application/json; charset=utf-8')
        return response, 200
