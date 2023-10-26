from flask import jsonify
from .exception import SauceNotFound,SauceValidationError

def handle_sauce_exceptions(app):
    @app.errorhandler(SauceValidationError)
    def handle_sauce_validation_error(e):
        return jsonify({"error": "Sauce validation error"}), 400

    
    @app.errorhandler(SauceNotFound)
    def handle_sauce_not_found(e):
        return jsonify({"error": "Sauce not found"}), 404
