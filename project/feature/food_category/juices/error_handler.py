from flask import jsonify
from .exception import JuiceNotFound,JuiceValidationError 

def handle_juice_exceptions(app):
    @app.errorhandler(JuiceValidationError)
    def handle_juice_validation_error(e):
        return jsonify({"error": "Juice validation error"}), 400

    
    @app.errorhandler(JuiceNotFound)
    def handle_juice_not_found(e):
        return jsonify({"error": "Juice not found"}), 404
