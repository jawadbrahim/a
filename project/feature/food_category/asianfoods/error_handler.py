from flask import jsonify
from .exception import AsianfoodNotFound,AsianfoodValidationError

def handle_asianfood_exceptions(app):
    @app.errorhandler(AsianfoodValidationError)
    def handle_asianfood_validation_error(e):
        return jsonify({"error": "Asianfood validation error"}), 400

    
    @app.errorhandler(AsianfoodNotFound)
    def handle_asianfood_not_found(e):
        return jsonify({"error": "Asianfood not found"}), 404
