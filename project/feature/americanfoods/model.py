from database.postgres import db 



class Americanfood(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(250))
    description = db.Column(db.Text)
    picture = db.Column(db.String(500))
    ingredients = db.Column(db.String(1000))