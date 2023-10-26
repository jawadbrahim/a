from flask import jsonify
from .exception import IcecreamNotFound,IcecreamValidationError 

def handle_icecream_exceptions(app):
    @app.errorhandler(IcecreamValidationError)
    def handle_icecream_validation_error(e):
        return jsonify({"error": "Icecream validation error"}), 400

    
    @app.errorhandler(IcecreamNotFound)
    def handle_icecream_not_found(e):
        return jsonify({"error": "Icecream not found"}), 404
