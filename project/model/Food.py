from database.postgres import db

class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250))
    description = db.Column(db.Text)
    picture = db.Column(db.String(500))
    ingredients = db.Column(db.String(1000))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category = db.relationship('Categories', back_populates='foods')

class Categories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)  
    foods = db.relationship('Food', back_populates='category')
