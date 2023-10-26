from flask import Response,request,json,jsonify
from project.feature.africanfoods.model import Africanfood
from database.postgres import db
from project.feature.africanfoods.schema import AfricanfoodSchema
from .decorators import validate_africanfood_existence
africanfood_schema = AfricanfoodSchema()
africanfoods_schema = AfricanfoodSchema(many=True)


def add_get_africanfoods():
    if request.method == "POST":
       
        africanfood_id = request.json.get("id")
        africanfoods_title = request.json.get("title")
        africanfoods_description = request.json.get("description")
        africanfoods_picture = request.json.get("picture")
        africanfoods_ingredients = request.json.get("ingredients")
        
        
        existing_africanfood = Africanfood.query.get(africanfood_id)

        if existing_africanfood:
            existing_africanfood.title = africanfoods_title
            existing_africanfood.description = africanfoods_description
            existing_africanfood.picture = africanfoods_picture
            existing_africanfood.ingredients = africanfoods_ingredients
        else:
            
            new_africanfood = Africanfood(
                id=africanfood_id,  
                title=africanfoods_title,
                description=africanfoods_description,
                picture=africanfoods_picture,
                ingredients=africanfoods_ingredients,
            )
            db.session.add(new_africanfood)

        db.session.commit()

        response_data = {
            "message": "created succefuly",
        }
        json_data = json.dumps(response_data, ensure_ascii=False)
        response = Response(json_data, content_type='application/json; charset=utf-8')
        return response, 201

    
    africanfoods_list = Africanfood.query.all()
    africanfoods = []

    for africanfood in africanfoods_list:
        africanfoods.append({
            "title": africanfood.title,
            "description": africanfood.description,
            "picture": africanfood.picture,
            "ingredients": africanfood.ingredients,
            
        })

    
    response_data = {"africanfoods": africanfoods}
    json_data = json.dumps(response_data, ensure_ascii=False)
    response = Response(json_data, content_type='application/json; charset=utf-8')
    return response


def update_africanfoods(africanfood_id):
    
    africanfoods_title = request.json["title"]
    africanfoods_description = request.json.get("description")
    africanfoods_picture = request.json.get("picture")
    africanfoods_ingredients = request.json.get("ingredients")

    africanfood = Africanfood.query.get(africanfood_id)

    if not africanfood:
        
        return jsonify({"message": "africanfood not found"}), 404

    
    africanfood.title = africanfoods_title
    africanfood.description = africanfoods_description
    africanfood.picture = africanfoods_picture
    africanfood.ingredients = africanfoods_ingredients

    
    db.session.commit()

    
    return jsonify({"message": "update succefuly"}), 200


@validate_africanfood_existence
def get_africanfoods(africanfood_id):
    africanfood = Africanfood.query.get(africanfood_id)
    if africanfood:
         
        response_data={
            "title": africanfood.title,
            "description": africanfood.description,
            "picture": africanfood.picture,
            "ingredients": africanfood.ingredients,
            
        }
        json_data = json.dumps(response_data, ensure_ascii=False)
        response = Response(json_data, content_type='application/json; charset=utf-8')
        return response

    return jsonify({"error": "Africanfoods not found"}), 404


def delete_africanfoods(africanfood_id):
    africanfood = Africanfood.query.get(africanfood_id)
    if africanfood:
        
        db.session.delete(africanfood)
        db.session.commit()
        return jsonify({"message": "delete succefuly"}), 200