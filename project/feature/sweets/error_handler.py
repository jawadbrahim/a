from flask import jsonify
from .exception import SweetNotFound,SweetValidationError

def handle_sweet_exceptions(app):
    @app.errorhandler(SweetValidationError)
    def handle_sweet_validation_error(e):
        return jsonify({"error": "Sweet validation error"}), 400

    
    @app.errorhandler(SweetNotFound)
    def handle_sweet_not_found(e):
        return jsonify({"error": "Sweet not found"}), 404
