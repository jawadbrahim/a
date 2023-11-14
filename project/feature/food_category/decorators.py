from functools import wraps
from flask import jsonify, request


required_properties_create_foods = ['title', 'description', 'picture', 'ingredients']

def validate_properties_existence(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        data = request.json
        missing_properties = [prop for prop in required_properties_create_foods if prop not in data]

        if missing_properties:
            return jsonify({"error": f"Missing properties: {', '.join(missing_properties)}"}), 400

        return func(*args, **kwargs)
    return wrapper
