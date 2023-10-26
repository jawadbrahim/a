from flask import Flask
from project.config.development import Development

def create_app(db):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = Development.DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JSON_AS_ASCII'] = False

    db.init_app(app)
    with app.app_context():
       

    
     from project.feature.arabicfoods.blueprints import arabicfoods_bp
     from project.feature.americanfoods.blueprints import americanfoods_bp
     from project.feature.africanfoods.blueprints import africanfoods_bp
     from project.feature.europeanfoods.blueprints import europeanfoods_bp
     from project.feature.asianfoods.blueprints import asianfoods_bp
     from project.feature.sweets.blueprints import sweets_bp
     from project.feature.salades.blueprints import salades_bp
     from project.feature.sauces.blueprints import sauces_bp
     from project.feature.juices.blueprints import juices_bp
     from project.feature.icecreams.blueprints import icecreams_bp

    
    app.register_blueprint(salades_bp, url_prefix="/salades")
    app.register_blueprint(icecreams_bp, url_prefix="/icecreams")
    app.register_blueprint(arabicfoods_bp, url_prefix="/arabicfoods")
    app.register_blueprint(europeanfoods_bp, url_prefix="/europeanfoods")
    app.register_blueprint(americanfoods_bp, url_prefix="/americanfoods")
    app.register_blueprint(africanfoods_bp, url_prefix="/africanfoods")
    app.register_blueprint(asianfoods_bp, url_prefix="/asianfoods")
    app.register_blueprint(juices_bp, url_prefix="/juices")
    app.register_blueprint(sauces_bp, url_prefix="/sauces")
    app.register_blueprint(sweets_bp, url_prefix="/sweets")
    
    return app