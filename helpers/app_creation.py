from flask import Flask
from dotenv import load_dotenv
import os

def create_app(db):
    load_dotenv()
    
    app = Flask(__name__)

    
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JSON_AS_ASCII'] = False

    
    db.init_app(app)

    
    from project.feature.food_category.blueprints import foods_bp
    
    app.register_blueprint(foods_bp, url_prefix="/foods")
    

    return app
