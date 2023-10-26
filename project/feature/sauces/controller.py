from flask import  request, Response, jsonify, json
from project.feature.sauces.model import Sauce
from project.feature.sauces.schema import SauceSchema
from project.cache.redis_cache import get_cached_data, set_cached_data
from database.postgres import db
from .decorators import validate_sauce_existence


sauce_schema = SauceSchema()
sauces_schema = SauceSchema(many=True)

def add_get_sauces():
    if request.method == "POST":
        sauce_id = request.json.get("id")
        sauces_title = request.json.get("title")
        sauces_description = request.json.get("description")
        sauces_picture = request.json.get("picture")
        sauces_ingredients = request.json.get("ingredients")
        
        existing_sauce = Sauce.query.get(sauce_id)

        if existing_sauce:
            existing_sauce.title = sauces_title
            existing_sauce.description = sauces_description
            existing_sauce.picture = sauces_picture
            existing_sauce.ingredients = sauces_ingredients
        else:
            new_sauce = Sauce(
                id=sauce_id,
                title=sauces_title,
                description=sauces_description,
                picture=sauces_picture,
                ingredients=sauces_ingredients,
            )
            db.session.add(new_sauce)

        db.session.commit()

        
        cache_key = f'sauce:{sauce_id}'
        set_cached_data(cache_key, "", expiration_time=3600)

        response_data = {
            "message": "created successfully",
        }
        json_data = json.dumps(response_data, ensure_ascii=False)
        response = Response(json_data, content_type='application/json; charset=utf-8')
        return response, 201

    sauces_list = Sauce.query.all()
    sauces = []

    for sauce in sauces_list:
        sauces.append({
            "title": sauce.title,
            "description": sauce.description,
            "picture": sauce.picture,
            "ingredients": sauce.ingredients,
        })

    response_data = {"sauces": sauces}
    json_data = json.dumps(response_data, ensure_ascii=False)
    response = Response(json_data, content_type='application/json; charset=utf-8')
    return response

def update_sauces(sauce_id):
    sauces_title = request.json["title"]
    sauces_description = request.json.get("description")
    sauces_picture = request.json.get("picture")
    sauces_ingredients = request.json.get("ingredients")

    sauce = Sauce.query.get(sauce_id)

    if not sauce:
        return jsonify({"message": "Sauce not found"}), 404

    sauce.title = sauces_title
    sauce.description = sauces_description
    sauce.picture = sauces_picture
    sauce.ingredients = sauces_ingredients

    db.session.commit()

    
    cache_key = f'sauce:{sauce_id}'
    set_cached_data(cache_key, "", expiration_time=3600)

    return jsonify({"message": "update successfully"}, 200)
@validate_sauce_existence
def get_sauces(sauce_id):
    cache_key = f'sauce:{sauce_id}'

    
    cached_data = get_cached_data(cache_key)

    if cached_data:
        return Response(cached_data, content_type='application/json; charset=utf-8')

    sauce = Sauce.query.get(sauce_id)

    if sauce:
        response_data = {
            "title": sauce.title,
            "description": sauce.description,
            "picture": sauce.picture,
            "ingredients": sauce.ingredients,
        }
        json_data = json.dumps(response_data, ensure_ascii=False)

        
        set_cached_data(cache_key, json_data)

        return Response(json_data, content_type='application/json; charset=utf-8')
    else:
        return jsonify({"error": "Sauce not found"}, 404)

def delete_sauces(sauce_id):
    sauce = Sauce.query.get(sauce_id)
    if sauce:
        db.session.delete(sauce)
        db.session.commit()

        
        cache_key = f'sauce:{sauce_id}'
        set_cached_data(cache_key, "", expiration_time=3600)

        return jsonify({"message": "delete successfully"}, 200)
