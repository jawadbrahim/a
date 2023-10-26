from flask import  request, Response, jsonify, json, Blueprint
from project.feature.juices.model import Juice
from project.feature.juices.schema import JuiceSchema
from project.cache.redis_cache import get_cached_data, set_cached_data
from database.postgres import db
from .decorators import validate_juice_existence

juice_schema = JuiceSchema()
juices_schema = JuiceSchema(many=True)

def add_get_juices():
    if request.method == "POST":
        juice_id = request.json.get("id")
        juices_title = request.json.get("title")
        juices_description = request.json.get("description")
        juices_picture = request.json.get("picture")
        juices_ingredients = request.json.get("ingredients")

        existing_juice = Juice.query.get(juice_id)

        if existing_juice:
            existing_juice.title = juices_title
            existing_juice.description = juices_description
            existing_juice.picture = juices_picture
            existing_juice.ingredients = juices_ingredients
        else:
            new_juice = Juice(
                id=juice_id,
                title=juices_title,
                description=juices_description,
                picture=juices_picture,
                ingredients=juices_ingredients,
            )
            db.session.add(new_juice)

        db.session.commit()

        cache_key = f'juice:{juice_id}'
        set_cached_data(cache_key, "", expiration_time=3600)

        response_data = {
            "message": "Juice created successfully",
        }
        json_data = json.dumps(response_data, ensure_ascii=False)
        response = Response(json_data, content_type='application/json; charset=utf-8')
        return response, 201

    juices_list = Juice.query.all()
    juices = []

    for juice in juices_list:
        juices.append({
            "title": juice.title,
            "description": juice.description,
            "picture": juice.picture,
            "ingredients": juice.ingredients,
        })

    response_data = {"juices": juices}
    json_data = json.dumps(response_data, ensure_ascii=False)
    response = Response(json_data, content_type='application/json; charset=utf-8')
    return response

def update_juices(juice_id):
    juices_title = request.json["title"]
    juices_description = request.json.get("description")
    juices_picture = request.json.get("picture")
    juices_ingredients = request.json.get("ingredients")

    juice = Juice.query.get(juice_id)

    if not juice:
        return jsonify({"message": "Juice not found"}), 404

    juice.title = juices_title
    juice.description = juices_description
    juice.picture = juices_picture
    juice.ingredients = juices_ingredients

    db.session.commit()

    cache_key = f'juice:{juice_id}'
    set_cached_data(cache_key, "", expiration_time=3600)

    return jsonify({"message": "Juice updated successfully"}, 200)
@validate_juice_existence
def get_juices(juice_id):
    cache_key = f'juice:{juice_id}'

    cached_data = get_cached_data(cache_key)

    if cached_data:
        return Response(cached_data, content_type='application/json; charset=utf-8')

    juice = Juice.query.get(juice_id)

    if juice:
        response_data = {
            "title": juice.title,
            "description": juice.description,
            "picture": juice.picture,
            "ingredients": juice.ingredients,
        }
        json_data = json.dumps(response_data, ensure_ascii=False)

        set_cached_data(cache_key, json_data)

        return Response(json_data, content_type='application/json; charset=utf-8')
    else:
        return jsonify({"error": "Juice not found"}, 404)

def delete_juices(juice_id):
    juice = Juice.query.get(juice_id)
    if juice:
        db.session.delete(juice)
        db.session.commit()

        cache_key = f'juice:{juice_id}'
        set_cached_data(cache_key, "", expiration_time=3600)

        return jsonify({"message": "Juice deleted successfully"}, 200)
    else:
        return jsonify({"message": "Juice not found"}, 404)
