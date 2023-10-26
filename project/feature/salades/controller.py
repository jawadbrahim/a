from flask import request, Response, jsonify, json
from project.feature.salades.model import Salade
from project.feature.salades.schema import SaladeSchema
from project.cache.redis_cache import get_cached_data, set_cached_data
from database.postgres import db
from .decorators import validate_salade_existence

salade_schema = SaladeSchema()
salades_schema = SaladeSchema(many=True)

def add_get_salades():
    if request.method == "POST":
        salade_id = request.json.get("id")
        salades_title = request.json.get("title")
        salades_description = request.json.get("description")
        salades_picture = request.json.get("picture")
        salades_ingredients = request.json.get("ingredients")
        
        existing_salade = Salade.query.get(salade_id)

        if existing_salade:
            existing_salade.title = salades_title
            existing_salade.description = salades_description
            existing_salade.picture = salades_picture
            existing_salade.ingredients = salades_ingredients
        else:
            new_salade = Salade(
                id=salade_id,
                title=salades_title,
                description=salades_description,
                picture=salades_picture,
                ingredients=salades_ingredients,
            )
            db.session.add(new_salade)

        db.session.commit()

        
        cache_key = f'salade:{salade_id}'
        set_cached_data(cache_key, "", expiration_time=3600)

        response_data = {
            "message": "created successfully",
        }
        json_data = json.dumps(response_data, ensure_ascii=False)
        response = Response(json_data, content_type='application/json; charset=utf-8')
        return response, 201

    salades_list = Salade.query.all()
    salades = []

    for salade in salades_list:
        salades.append({
            "title": salade.title,
            "description": salade.description,
            "picture": salade.picture,
            "ingredients": salade.ingredients,
        })

    response_data = {"salades": salades}
    json_data = json.dumps(response_data, ensure_ascii=False)
    response = Response(json_data, content_type='application/json; charset=utf-8')
    return response

def update_salades(salade_id):
    salades_title = request.json["title"]
    salades_description = request.json.get("description")
    salades_picture = request.json.get("picture")
    salades_ingredients = request.json.get("ingredients")

    salade = Salade.query.get(salade_id)

    if not salade:
        return jsonify({"message": "Salade not found"}), 404

    salade.title = salades_title
    salade.description = salades_description
    salade.picture = salades_picture
    salade.ingredients = salades_ingredients

    db.session.commit()

    
    cache_key = f'salade:{salade_id}'
    set_cached_data(cache_key, "", expiration_time=3600)

    return jsonify({"message": "update successfully"}, 200)
@validate_salade_existence
def get_salades(salade_id):
    cache_key = f'salade:{salade_id}'

    
    cached_data = get_cached_data(cache_key)

    if cached_data:
        return Response(cached_data, content_type='application/json; charset=utf-8')

    salade = Salade.query.get(salade_id)

    if salade:
        response_data = {
            "title": salade.title,
            "description": salade.description,
            "picture": salade.picture,
            "ingredients": salade.ingredients,
        }
        json_data = json.dumps(response_data, ensure_ascii=False)

        
        set_cached_data(cache_key, json_data)

        return Response(json_data, content_type='application/json; charset=utf-8')
    else:
        return jsonify({"error": "Salade not found"}, 404)

def delete_salades(salade_id):
    salade = Salade.query.get(salade_id)
    if salade:
        db.session.delete(salade)
        db.session.commit()

        
        cache_key = f'salade:{salade_id}'
        set_cached_data(cache_key, "", expiration_time=3600)

        return jsonify({"message": "delete successfully"}, 200)
