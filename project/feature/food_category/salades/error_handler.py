from flask import jsonify
from .exception import SaladeNotFound,SaladeValidationError

def handle_salade_exceptions(app):
    @app.errorhandler(SaladeValidationError)
    def handle_salade_validation_error(e):
        return jsonify({"error": "Salade validation error"}), 400

    
    @app.errorhandler(SaladeNotFound)
    def handle_salade_not_found(e):
        return jsonify({"error": "Salade not found"}), 404
