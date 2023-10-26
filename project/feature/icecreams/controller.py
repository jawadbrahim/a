from flask import request, Response, json, jsonify
from project.feature.icecreams.model import Icecream
from database.postgres import db
from project.feature.icecreams.schema import IcecreamSchema
from project.cache.redis_cache import get_cached_data, set_cached_data
from .decorators import validate_icecream_existence

icecream_schema = IcecreamSchema()
icecreams_schema = IcecreamSchema(many=True)

def add_get_icecreams():
    if request.method == "POST":
        icecream_id = request.json.get("id")
        icecreams_title = request.json.get("title")
        icecreams_description = request.json.get("description")
        icecreams_picture = request.json.get("picture")
        icecreams_ingredients = request.json.get("ingredients")

        existing_icecream = Icecream.query.get(icecream_id)

        if existing_icecream:
            existing_icecream.title = icecreams_title
            existing_icecream.description = icecreams_description
            existing_icecream.picture = icecreams_picture
            existing_icecream.ingredients = icecreams_ingredients
        else:
            new_icecream = Icecream(
                id=icecream_id,
                title=icecreams_title,
                description=icecreams_description,
                picture=icecreams_picture,
                ingredients=icecreams_ingredients,
            )
            db.session.add(new_icecream)

        db.session.commit()

        cache_key = f'icecream:{icecream_id}'
        set_cached_data(cache_key, "", expiration_time=3600)

        response_data = {
            "message": "created successfully",
        }
        json_data = json.dumps(response_data, ensure_ascii=False)
        response = Response(json_data, content_type='application/json; charset=utf-8')
        return response, 201

    icecreams_list = Icecream.query.all()
    icecreams = []

    for icecream in icecreams_list:
        icecreams.append({
            "title": icecream.title,
            "description": icecream.description,
            "picture": icecream.picture,
            "ingredients": icecream.ingredients,
        })

    response_data = {"icecreams": icecreams}
    json_data = json.dumps(response_data, ensure_ascii=False)
    response = Response(json_data, content_type='application/json; charset=utf-8')
    return response

def update_icecreams(icecream_id):
    icecreams_title = request.json["title"]
    icecreams_description = request.json.get("description")
    icecreams_picture = request.json.get("picture")
    icecreams_ingredients = request.json.get("ingredients")

    icecream = Icecream.query.get(icecream_id)

    if not icecream:
        return jsonify({"message": "Icecream not found"}), 404

    icecream.title = icecreams_title
    icecream.description = icecreams_description
    icecream.picture = icecreams_picture
    icecream.ingredients = icecreams_ingredients

    db.session.commit()

    cache_key = f'icecream:{icecream_id}'
    set_cached_data(cache_key, "", expiration_time=3600)

    return jsonify({"message": "update successfully"}, 200)
@validate_icecream_existence
def get_icecreams(icecream_id):
    cache_key = f'icecream:{icecream_id}'

    cached_data = get_cached_data(cache_key)

    if cached_data:
        return Response(cached_data, content_type='application/json; charset=utf-8')

    icecream = Icecream.query.get(icecream_id)

    if icecream:
        response_data = {
            "title": icecream.title,
            "description": icecream.description,
            "picture": icecream.picture,
            "ingredients": icecream.ingredients,
        }
        json_data = json.dumps(response_data, ensure_ascii=False)

        set_cached_data(cache_key, json_data)

        return Response(json_data, content_type='application/json; charset=utf-8')
    else:
        return jsonify({"error": "Icecream not found"}, 404)

def delete_icecreams(icecream_id):
    icecream = Icecream.query.get(icecream_id)
    if icecream:
        db.session.delete(icecream)
        db.session.commit()

        cache_key = f'icecream:{icecream_id}'
        set_cached_data(cache_key, "", expiration_time=3600)

        return jsonify({"message": "delete successfully"}, 200)
