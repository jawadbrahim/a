from flask import Response, request, json, jsonify
from project.model.salades import Salade
from database.postgres import db
from project.feature.food_category.salades.schema import SaladeSchema
from project.cache.redis_cache import get_cached_data, set_cached_data
from .decorators import validate_salade_existence

salade_schema = SaladeSchema()
salades_schema = SaladeSchema(many=True)

def create_salade():
    if request.method == "POST":
        salade_data = salade_schema.load(request.json)
        new_salade = Salade(**salade_data)
        db.session.add(new_salade)
        db.session.commit()

        cache_key = f'salade:{new_salade.id}'
        set_cached_data(cache_key, "", expiration_time=3600)

        response_data = {
            "message": "Created successfully",
            "food_categories": None  
        }
        json_data = json.dumps(response_data, ensure_ascii=False)
        response = Response(json_data, content_type='application/json; charset=utf-8')
        return response, 201

def get_salades_list():
    salades_list = Salade.query.all()
    salades = []

    for salade in salades_list:
        salades.append({
            "title": salade.title,
            "description": salade.description,
            "picture": salade.picture,
            "ingredients": salade.ingredients,
        })

    response_data = {"food_categories": {"salades":salades}} 
    json_data = json.dumps(response_data, ensure_ascii=False)
    response = Response(json_data, content_type='application/json; charset=utf-8')
    return response

def update_salades(salade_id):
    salade_data = salade_schema.load(request.json)

    salade = Salade.query.get(salade_id)

    salade.title = salade_data["title"]
    salade.description = salade_data.get("description")
    salade.picture = salade_data.get("picture")
    salade.ingredients = salade_data.get("ingredients")

    db.session.commit()

    cache_key = f'salade:{salade_id}'
    set_cached_data(cache_key, "", expiration_time=3600)

    response_data = {
        "message": "Update successfully",
        "food_categories": None  
    }
    json_data = json.dumps(response_data, ensure_ascii=False)
    response = Response(json_data, content_type='application/json; charset=utf-8')
    return response, 200

@validate_salade_existence
def get_salade_single(salade_id):
    cache_key = f'salade:{salade_id}'
    cached_data = get_cached_data(cache_key)

    if cached_data:
        response = Response(cached_data, content_type='application/json; charset=utf-8')
        return response

    salade = Salade.query.get(salade_id)

    if salade:
        response_data = salade_schema.dump(salade)

        set_cached_data(cache_key, response_data)

        json_data = json.dumps(response_data, ensure_ascii=False)
        response = Response(json_data, content_type='application/json; charset=utf-8')
        return response
    else:
        response_data = {"food_categories": {"error": "Salade not found"}}  
        json_data = json.dumps(response_data, ensure_ascii=False)
        response = Response(json_data, content_type='application/json; charset=utf-8')
        return response, 404

def delete_salades(salade_id):
    salade = Salade.query.get(salade_id)
    if salade:
        db.session.delete(salade)
        db.session.commit()

        cache_key = f'salade:{salade_id}'
        set_cached_data(cache_key, "", expiration_time=3600)

        response_data = {
            "message": "Delete successfully",
            "food_categories": None  
        }
        json_data = json.dumps(response_data, ensure_ascii=False)
        response = Response(json_data, content_type='application/json; charset=utf-8')
        return response, 200
