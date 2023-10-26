from flask import jsonify
from .exception import AmericanfoodNotFound,AmericanfoodValidationError 

def handle_americanfood_exceptions(app):
    @app.errorhandler(AmericanfoodValidationError)
    def handle_americanfood_validation_error(e):
        return jsonify({"error": "Americanfood validation error"}), 400

    
    @app.errorhandler(AmericanfoodNotFound)
    def handle_americanfood_not_found(e):
        return jsonify({"error": "Americanfood not found"}), 404
