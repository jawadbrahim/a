from flask import Response, json, jsonify, request
from project.feature.americanfoods.model import Americanfood
from project.feature.americanfoods.schema import AmericanfoodSchema
from project.cache.redis_cache import get_cached_data, set_cached_data
from database.postgres import db
from .decorators import validate_americanfood_existence
americanfood_schema = AmericanfoodSchema()
americanfoods_schema = AmericanfoodSchema(many=True)

def add_get_americanfoods():
    if request.method == "POST":
        americanfood_id = request.json.get("id")
        americanfoods_title = request.json.get("title")
        americanfoods_description = request.json.get("description")
        americanfoods_picture = request.json.get("picture")
        americanfoods_ingredients = request.json.get("ingredients")

        existing_americanfood = Americanfood.query.get(americanfood_id)

        if existing_americanfood:
            existing_americanfood.title = americanfoods_title
            existing_americanfood.description = americanfoods_description
            existing_americanfood.picture = americanfoods_picture
            existing_americanfood.ingredients = americanfoods_ingredients
        else:
            new_americanfood = Americanfood(
                id=americanfood_id,
                title=americanfoods_title,
                description=americanfoods_description,
                picture=americanfoods_picture,
                ingredients=americanfoods_ingredients,
            )
            db.session.add(new_americanfood)

        db.session.commit()

        cache_key = f'americanfood:{americanfood_id}'
        set_cached_data(cache_key, "", expiration_time=3600)

        response_data = {
            "message": "created successfully",
        }
        json_data = json.dumps(response_data, ensure_ascii=False)
        response = Response(json_data, content_type='application/json; charset=utf-8')
        return response, 201

    americanfoods_list = Americanfood.query.all()
    americanfoods = []

    for americanfood in americanfoods_list:
        americanfoods.append({
            "title": americanfood.title,
            "description": americanfood.description,
            "picture": americanfood.picture,
            "ingredients": americanfood.ingredients,
        })

    response_data = {"americanfoods": americanfoods}
    json_data = json.dumps(response_data, ensure_ascii=False)
    response = Response(json_data, content_type='application/json; charset=utf-8')
    return response

def update_americanfoods(americanfood_id):
    americanfoods_title = request.json["title"]
    americanfoods_description = request.json.get("description")
    americanfoods_picture = request.json.get("picture")
    americanfoods_ingredients = request.json.get("ingredients")

    americanfood = Americanfood.query.get(americanfood_id)

    if not americanfood:
        return jsonify({"message": "Americanfood not found"}), 404

    americanfood.title = americanfoods_title
    americanfood.description = americanfoods_description
    americanfood.picture = americanfoods_picture
    americanfood.ingredients = americanfoods_ingredients

    db.session.commit()

    cache_key = f'americanfood:{americanfood_id}'
    set_cached_data(cache_key, "", expiration_time=3600)

    return jsonify({"message": "update successfully"}, 200)
@validate_americanfood_existence
def get_americanfoods(americanfood_id):
    cache_key = f'americanfood:{americanfood_id}'

    cached_data = get_cached_data(cache_key)

    if cached_data:
        return Response(cached_data, content_type='application/json; charset=utf-8')

    americanfood = Americanfood.query.get(americanfood_id)

    if americanfood:
        response_data = {
            "title": americanfood.title,
            "description": americanfood.description,
            "picture": americanfood.picture,
            "ingredients": americanfood.ingredients,
        }
        json_data = json.dumps(response_data, ensure_ascii=False)

        set_cached_data(cache_key, json_data)

        return Response(json_data, content_type='application/json; charset=utf-8')
    else:
        return jsonify({"error": "Americanfood not found"}, 404)

def delete_americanfoods(americanfood_id):
    americanfood = Americanfood.query.get(americanfood_id)
    if americanfood:
        db.session.delete(americanfood)
        db.session.commit()

        cache_key = f'americanfood:{americanfood_id}'
        set_cached_data(cache_key, "", expiration_time=3600)

        return jsonify({"message": "delete successfully"}, 200)
