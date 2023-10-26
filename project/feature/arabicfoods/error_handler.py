from flask import jsonify
from .exception import ArabicfoodValidationError, ArabicfoodNotFound  

def handle_arabicfood_exceptions(app):
    @app.errorhandler(ArabicfoodValidationError)
    def handle_arabicfood_validation_error(e):
        return jsonify({"error": "Arabicfood validation error"}), 400

    
    @app.errorhandler(ArabicfoodNotFound)
    def handle_arabicfood_not_found(e):
        return jsonify({"error": "Arabicfood not found"}), 404
