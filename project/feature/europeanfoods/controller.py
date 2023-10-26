from flask import request, Response, json, jsonify
from project.feature.europeanfoods.model import Europeanfood
from database.postgres import db
from project.feature.europeanfoods.schema import EuropeanfoodSchema
from project.cache.redis_cache import get_cached_data, set_cached_data
from .decorators import validate_europeanfood_existence
europeanfood_schema = EuropeanfoodSchema()
europeanfoods_schema = EuropeanfoodSchema(many=True)

def add_get_europeanfoods():
    if request.method == "POST":
        europeanfood_id = request.json.get("id")
        europeanfoods_title = request.json.get("title")
        europeanfoods_description = request.json.get("description")
        europeanfoods_picture = request.json.get("picture")
        europeanfoods_ingredients = request.json.get("ingredients")

        existing_europeanfood = Europeanfood.query.get(europeanfood_id)

        if existing_europeanfood:
            existing_europeanfood.title = europeanfoods_title
            existing_europeanfood.description = europeanfoods_description
            existing_europeanfood.picture = europeanfoods_picture
            existing_europeanfood.ingredients = europeanfoods_ingredients
        else:
            new_europeanfood = Europeanfood(
                id=europeanfood_id,
                title=europeanfoods_title,
                description=europeanfoods_description,
                picture=europeanfoods_picture,
                ingredients=europeanfoods_ingredients,
            )
            db.session.add(new_europeanfood)

        db.session.commit()

        cache_key = f'europeanfood:{europeanfood_id}'
        set_cached_data(cache_key, "", expiration_time=3600)

        response_data = {
            "message": "created successfully",
        }
        json_data = json.dumps(response_data, ensure_ascii=False)
        response = Response(json_data, content_type='application/json; charset=utf-8')
        return response, 201

    europeanfoods_list = Europeanfood.query.all()
    europeanfoods = []

    for europeanfood in europeanfoods_list:
        europeanfoods.append({
            "title": europeanfood.title,
            "description": europeanfood.description,
            "picture": europeanfood.picture,
            "ingredients": europeanfood.ingredients,
        })

    response_data = {"europeanfoods": europeanfoods}
    json_data = json.dumps(response_data, ensure_ascii=False)
    response = Response(json_data, content_type='application/json; charset=utf-8')
    return response

def update_europeanfoods(europeanfood_id):
    europeanfoods_title = request.json["title"]
    europeanfoods_description = request.json.get("description")
    europeanfoods_picture = request.json.get("picture")
    europeanfoods_ingredients = request.json.get("ingredients")

    europeanfood = Europeanfood.query.get(europeanfood_id)

    if not europeanfood:
        return jsonify({"message": "Europeanfood not found"}), 404

    europeanfood.title = europeanfoods_title
    europeanfood.description = europeanfoods_description
    europeanfood.picture = europeanfoods_picture
    europeanfood.ingredients = europeanfoods_ingredients

    db.session.commit()

    cache_key = f'europeanfood:{europeanfood_id}'
    set_cached_data(cache_key, "", expiration_time=3600)

    return jsonify({"message": "update successfully"}, 200)
@validate_europeanfood_existence
def get_europeanfoods(europeanfood_id):
    cache_key = f'europeanfood:{europeanfood_id}'

    cached_data = get_cached_data(cache_key)

    if cached_data:
        return Response(cached_data, content_type='application/json; charset=utf-8')

    europeanfood = Europeanfood.query.get(europeanfood_id)

    if europeanfood:
        response_data = {
            "title": europeanfood.title,
            "description": europeanfood.description,
            "picture": europeanfood.picture,
            "ingredients": europeanfood.ingredients,
        }
        json_data = json.dumps(response_data, ensure_ascii=False)

        set_cached_data(cache_key, json_data)

        return Response(json_data, content_type='application/json; charset=utf-8')
    else:
        return jsonify({"error": "Europeanfood not found"}, 404)

def delete_europeanfoods(europeanfood_id):
    europeanfood = Europeanfood.query.get(europeanfood_id)
    if europeanfood:
        db.session.delete(europeanfood)
        db.session.commit()

        cache_key = f'europeanfood:{europeanfood_id}'
        set_cached_data(cache_key, "", expiration_time=3600)

        return jsonify({"message": "delete successfully"}, 200)
