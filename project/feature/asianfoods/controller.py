from flask import  request, Response, jsonify, json
from project.feature.asianfoods.model import Asianfood
from project.feature.asianfoods.schema import AsianfoodSchema
from project.cache.redis_cache import get_cached_data, set_cached_data
from database.postgres import db
from .decorators import validate_asianfood_existence

asianfood_schema = AsianfoodSchema()
asianfoods_schema = AsianfoodSchema(many=True)

def add_get_asianfoods():
    if request.method == "POST":
        asianfood_id = request.json.get("id")
        asianfoods_title = request.json.get("title")
        asianfoods_description = request.json.get("description")
        asianfoods_picture = request.json.get("picture")
        asianfoods_ingredients = request.json.get("ingredients")
        
        existing_asianfood = Asianfood.query.get(asianfood_id)

        if existing_asianfood:
            existing_asianfood.title = asianfoods_title
            existing_asianfood.description = asianfoods_description
            existing_asianfood.picture = asianfoods_picture
            existing_asianfood.ingredients = asianfoods_ingredients
        else:
            new_asianfood = Asianfood(
                id=asianfood_id,
                title=asianfoods_title,
                description=asianfoods_description,
                picture=asianfoods_picture,
                ingredients=asianfoods_ingredients,
            )
            db.session.add(new_asianfood)

        db.session.commit()

        cache_key = f'asianfood:{asianfood_id}'
        set_cached_data(cache_key, "", expiration_time=3600)

        response_data = {
            "message": "created successfully",
        }
        json_data = json.dumps(response_data, ensure_ascii=False)
        response = Response(json_data, content_type='application/json; charset=utf-8')
        return response, 201

    asianfoods_list = Asianfood.query.all()
    asianfoods = []

    for asianfood in asianfoods_list:
        asianfoods.append({
            "title": asianfood.title,
            "description": asianfood.description,
            "picture": asianfood.picture,
            "ingredients": asianfood.ingredients,
        })

    response_data = {"asianfoods": asianfoods}
    json_data = json.dumps(response_data, ensure_ascii=False)
    response = Response(json_data, content_type='application/json; charset=utf-8')
    return response

def update_asianfoods(asianfood_id):
    asianfoods_title = request.json["title"]
    asianfoods_description = request.json.get("description")
    asianfoods_picture = request.json.get("picture")
    asianfoods_ingredients = request.json.get("ingredients")

    asianfood = Asianfood.query.get(asianfood_id)

    if not asianfood:
        return jsonify({"message": "Asianfood not found"}), 404

    asianfood.title = asianfoods_title
    asianfood.description = asianfoods_description
    asianfood.picture = asianfoods_picture
    asianfood.ingredients = asianfoods_ingredients

    db.session.commit()

    cache_key = f'asianfood:{asianfood_id}'
    set_cached_data(cache_key, "", expiration_time=3600)

    return jsonify({"message": "update successfully"}, 200)
@validate_asianfood_existence
def get_asianfoods(asianfood_id):
    cache_key = f'asianfood:{asianfood_id}'

    cached_data = get_cached_data(cache_key)

    if cached_data:
        return Response(cached_data, content_type='application/json; charset=utf-8')

    asianfood = Asianfood.query.get(asianfood_id)

    if asianfood:
        response_data = {
            "title": asianfood.title,
            "description": asianfood.description,
            "picture": asianfood.picture,
            "ingredients": asianfood.ingredients,
        }
        json_data = json.dumps(response_data, ensure_ascii=False)

        set_cached_data(cache_key, json_data)

        return Response(json_data, content_type='application/json; charset=utf-8')
    else:
        return jsonify({"error": "Asianfood not found"}, 404)

def delete_asianfoods(asianfood_id):
    asianfood = Asianfood.query.get(asianfood_id)
    if asianfood:
        db.session.delete(asianfood)
        db.session.commit()

        cache_key = f'asianfood:{asianfood_id}'
        set_cached_data(cache_key, "", expiration_time=3600)

        return jsonify({"message": "delete successfully"}, 200)
