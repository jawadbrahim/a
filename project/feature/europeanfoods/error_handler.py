from flask import jsonify
from .exception import EuropeanfoodNotFound,EuropeanfoodValidationError

def handle_europeanfood_exceptions(app):
    @app.errorhandler(EuropeanfoodValidationError)
    def handle_europeanfood_validation_error(e):
        return jsonify({"error": "European validation error"}), 400

    
    @app.errorhandler(EuropeanfoodNotFound)
    def handle_europeanfood_not_found(e):
        return jsonify({"error": "Europeanfood not found"}), 404
