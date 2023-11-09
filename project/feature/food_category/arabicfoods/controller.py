from flask import request, Response, jsonify, json
from project.model.arabicfoods import Arabicfood
from project.feature.food_category.arabicfoods.schema import ArabicfoodSchema
from project.cache.redis_cache import get_cached_data, set_cached_data
from .decorators import validate_arabicfood_existence 
from database.postgres import db


arabicfood_schema = ArabicfoodSchema()
arabicfoods_schema = ArabicfoodSchema(many=True)


def create_arabicfood():
    if request.method == "POST":
        arabicfood_data = arabicfood_schema.load(request.json)
        new_arabicfood = Arabicfood(**arabicfood_data)
        db.session.add(new_arabicfood)
        db.session.commit()

        cache_key = f'arabicfood:{new_arabicfood.id}'
        set_cached_data(cache_key, "", expiration_time=3600)

        response_data = {
            "message": "Created successfully",
            "food_categories": None
        }
        json_data = json.dumps(response_data, ensure_ascii=False)
        response = Response(json_data, content_type='application/json; charset=utf-8')
        return response, 201


def get_arabicfoods_list():
    arabicfoods_list = Arabicfood.query.all()
    arabicfoods = []

    for arabicfood in arabicfoods_list:
        arabicfoods.append({
            "title": arabicfood.title,
            "description": arabicfood.description,
            "picture": arabicfood.picture,
            "ingredients": arabicfood.ingredients,
        })

    response_data = {"message": None, "food_categories": {"arabicfoods": arabicfoods}}
    json_data = json.dumps(response_data, ensure_ascii=False)
    response = Response(json_data, content_type='application/json; charset=utf-8')
    return response


def update_arabicfoods(arabicfood_id):
    arabicfood_data = arabicfood_schema.load(request.json)

    arabicfood = Arabicfood.query.get(arabicfood_id)

    arabicfood.title = arabicfood_data["title"]
    arabicfood.description = arabicfood_data.get("description")
    arabicfood.picture = arabicfood_data.get("picture")
    arabicfood.ingredients = arabicfood_data.get("ingredients")

    db.session.commit()

    cache_key = f'arabicfood:{arabicfood_id}'
    set_cached_data(cache_key, "", expiration_time=3600)

    response_data = {
        "message": "Update successfully",
        "food_categories": None
    }
    json_data = json.dumps(response_data, ensure_ascii=False)
    response = Response(json_data, content_type='application/json; charset=utf-8')
    return response, 200


@validate_arabicfood_existence
def get_arabicfood_single(arabicfood_id):
    cache_key = f'arabicfood:{arabicfood_id}'
    cached_data = get_cached_data(cache_key)

    if cached_data:
        response = Response(cached_data, content_type='application/json; charset=utf-8')
        return response

    arabicfood = Arabicfood.query.get(arabicfood_id)

    if arabicfood:
        response_data = arabicfood_schema.dump(arabicfood)

        set_cached_data(cache_key, response_data)

        json_data = json.dumps(response_data, ensure_ascii=False)
        response = Response(json_data, content_type='application/json; charset=utf-8')
        return response
    else:
        response_data = {"message": None, "food_categories": {"error": "Arabicfood not found"}}
        json_data = json.dumps(response_data, ensure_ascii=False)
        response = Response(json_data, content_type='application/json; charset=utf-8')
        return response, 404


def delete_arabicfoods(arabicfood_id):
    arabicfood = Arabicfood.query.get(arabicfood_id)
    if arabicfood:
        db.session.delete(arabicfood)
        db.session.commit()

        cache_key = f'arabicfood:{arabicfood_id}'
        set_cached_data(cache_key, "", expiration_time=3600)

        response_data = {
            "message": "Delete successfully",
            "food_categories": None
        }
        json_data = json.dumps(response_data, ensure_ascii=False)
        response = Response(json_data, content_type='application/json; charset=utf-8')
        return response, 200
