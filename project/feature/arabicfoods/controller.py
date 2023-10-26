from flask import request, Response, jsonify, json
from project.feature.arabicfoods.model import Arabicfood
from project.feature.arabicfoods.schema import ArabicfoodSchema
from project.cache.redis_cache import get_cached_data, set_cached_data
from .decorators import validate_arabicfood_existence 
from database.postgres import db

arabicfood_schema = ArabicfoodSchema()
arabicfoods_schema = ArabicfoodSchema(many=True)

def add_get_arabicfoods():
    if request.method == "POST":
        arabicfood_id = request.json.get("id")
        arabicfoods_title = request.json.get("title")
        arabicfoods_description = request.json.get("description")
        arabicfoods_picture = request.json.get("picture")
        arabicfoods_ingredients = request.json.get("ingredients")
        
        existing_arabicfood = Arabicfood.query.get(arabicfood_id)

        if existing_arabicfood:
            existing_arabicfood.title = arabicfoods_title
            existing_arabicfood.description = arabicfoods_description
            existing_arabicfood.picture = arabicfoods_picture
            existing_arabicfood.ingredients = arabicfoods_ingredients
        else:
            new_arabicfood = Arabicfood(
                id=arabicfood_id,
                title=arabicfoods_title,
                description=arabicfoods_description,
                picture=arabicfoods_picture,
                ingredients=arabicfoods_ingredients,
            )
            db.session.add(new_arabicfood)

        db.session.commit()

        
        cache_key = f'arabicfood:{arabicfood_id}'
        set_cached_data(cache_key, "", expiration_time=3600)

        response_data = {
            "message": "created successfully",
        }
        json_data = json.dumps(response_data, ensure_ascii=False)
        response = Response(json_data, content_type='application/json; charset=utf-8')
        return response, 201

    arabicfoods_list = Arabicfood.query.all()
    arabicfoods = []

    for arabicfood in arabicfoods_list:
        arabicfoods.append({
            "title": arabicfood.title,
            "description": arabicfood.description,
            "picture": arabicfood.picture,
            "ingredients": arabicfood.ingredients,
        })

    response_data = {"arabicfoods": arabicfoods}
    json_data = json.dumps(response_data, ensure_ascii=False)
    response = Response(json_data, content_type='application/json; charset=utf-8')
    return response

def update_arabicfoods(arabicfood_id):
    arabicfoods_title = request.json["title"]
    arabicfoods_description = request.json.get("description")
    arabicfoods_picture = request.json.get("picture")
    arabicfoods_ingredients = request.json.get("ingredients")

    arabicfood = Arabicfood.query.get(arabicfood_id)

    

    arabicfood.title = arabicfoods_title
    arabicfood.description = arabicfoods_description
    arabicfood.picture = arabicfoods_picture
    arabicfood.ingredients = arabicfoods_ingredients

    db.session.commit()

    
    cache_key = f'arabicfood:{arabicfood_id}'
    set_cached_data(cache_key, "", expiration_time=3600)

    return jsonify({"message": "update successfully"}, 200)

@validate_arabicfood_existence
def get_arabicfoods(arabicfood_id):
    cache_key = f'arabicfood:{arabicfood_id}'

    cached_data = get_cached_data(cache_key)

    if cached_data:
        return Response(cached_data, content_type='application/json; charset=utf-8')

    arabicfood = Arabicfood.query.get(arabicfood_id)

    if arabicfood:
        response_data = {
            "title": arabicfood.title,
            "description": arabicfood.description,
            "picture": arabicfood.picture,
            "ingredients": arabicfood.ingredients,
        }
        json_data = json.dumps(response_data, ensure_ascii=False)

        set_cached_data(cache_key, json_data)

        return Response(json_data, content_type='application/json; charset=utf-8')
    else:
        return jsonify({"error": "Arabicfood not found"}, 404)
def delete_arabicfoods(arabicfood_id):
    arabicfood = Arabicfood.query.get(arabicfood_id)
    if arabicfood:
        db.session.delete(arabicfood)
        db.session.commit()

        
        cache_key = f'arabicfood:{arabicfood_id}'
        set_cached_data(cache_key, "", expiration_time=3600)

        return jsonify({"message": "delete successfully"}, 200)
