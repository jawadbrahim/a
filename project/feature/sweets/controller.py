from flask import request, Response, jsonify, json
from project.feature.sweets.model import Sweet
from project.feature.sweets.schema import SweetSchema
from project.cache.redis_cache import get_cached_data, set_cached_data
from database.postgres import db
from .decorators import validate_sweet_existence
sweet_schema = SweetSchema()
sweets_schema = SweetSchema(many=True)

def add_get_sweets():
    if request.method == "POST":
        sweet_id = request.json.get("id")
        sweets_title = request.json.get("title")
        sweets_description = request.json.get("description")
        sweets_picture = request.json.get("picture")
        sweets_ingredients = request.json.get("ingredients")

        existing_sweet = Sweet.query.get(sweet_id)

        if existing_sweet:
            existing_sweet.title = sweets_title
            existing_sweet.description = sweets_description
            existing_sweet.picture = sweets_picture
            existing_sweet.ingredients = sweets_ingredients
        else:
            new_sweet = Sweet(
                id=sweet_id,
                title=sweets_title,
                description=sweets_description,
                picture=sweets_picture,
                ingredients=sweets_ingredients,
            )
            db.session.add(new_sweet)

        db.session.commit()

        cache_key = f'sweet:{sweet_id}'
        set_cached_data(cache_key, "", expiration_time=3600)

        response_data = {
            "message": "created successfully",
        }
        json_data = json.dumps(response_data, ensure_ascii=False)
        response = Response(json_data, content_type='application/json; charset=utf-8')
        return response, 201

    sweets_list = Sweet.query.all()
    sweets = []

    for sweet in sweets_list:
        sweets.append({
            "title": sweet.title,
            "description": sweet.description,
            "picture": sweet.picture,
            "ingredients": sweet.ingredients,
        })

    response_data = {"sweets": sweets}
    json_data = json.dumps(response_data, ensure_ascii=False)
    response = Response(json_data, content_type='application/json; charset=utf-8')
    return response

def update_sweets(sweet_id):
    sweets_title = request.json["title"]
    sweets_description = request.json.get("description")
    sweets_picture = request.json.get("picture")
    sweets_ingredients = request.json.get("ingredients")

    sweet = Sweet.query.get(sweet_id)

    if not sweet:
        return jsonify({"message": "Sweet not found"}), 404

    sweet.title = sweets_title
    sweet.description = sweets_description
    sweet.picture = sweets_picture
    sweet.ingredients = sweets_ingredients

    db.session.commit()

    cache_key = f'sweet:{sweet_id}'
    set_cached_data(cache_key, "", expiration_time=3600)

    return jsonify({"message": "update successfully"}, 200)
@validate_sweet_existence
def get_sweets(sweet_id):
    cache_key = f'sweet:{sweet_id}'
    cached_data = get_cached_data(cache_key)

    if cached_data:
        return Response(cached_data, content_type='application/json; charset=utf-8')

    sweet = Sweet.query.get(sweet_id)

    if sweet:
        response_data = {
            "title": sweet.title,
            "description": sweet.description,
            "picture": sweet.picture,
            "ingredients": sweet.ingredients,
        }
        json_data = json.dumps(response_data, ensure_ascii=False)

        set_cached_data(cache_key, json_data)

        return Response(json_data, content_type='application/json; charset=utf-8')
    else:
        return jsonify({"error": "Sweet not found"}, 404)

def delete_sweets(sweet_id):
    sweet = Sweet.query.get(sweet_id)

    if sweet:
        db.session.delete(sweet)
        db.session.commit()

        cache_key = f'sweet:{sweet_id}'
        set_cached_data(cache_key, "", expiration_time=3600)

        return jsonify({"message": "delete successfully"}, 200)
