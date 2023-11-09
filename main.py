from flask import  jsonify
from database.postgres import db
from helpers.app_creation import create_app
from marshmallow import ValidationError
from flask_migrate import Migrate

app = create_app(db)
migrate = Migrate(app,db)
@app.errorhandler(ValidationError)
def handle_validation_error(error):
    return jsonify(error.messages), 400

if __name__ == '__main__':
    app.run(debug=True)