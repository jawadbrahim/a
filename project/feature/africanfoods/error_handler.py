from flask import jsonify
from .exception import AfricanfoodValidationError,AfricanfoodNotFound

def handle_africanfood_exceptions(app):
    @app.errorhandler(AfricanfoodValidationError)
    def handle_africanfood_validation_error(e):
        return jsonify({"error": "Africanfood validation error"}), 400

    
    @app.errorhandler(AfricanfoodNotFound)
    def handle_africanfood_not_found(e):
        return jsonify({"error": "Africanfood not found"}), 404
