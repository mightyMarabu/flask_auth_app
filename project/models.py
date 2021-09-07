from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    content = db.Column(db.String(100)) 

class Point(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lng = db.Column(db.Float)
    lat = db.Column(db.Float)
    name = db.Column(db.String(100))

#class PointSchema(ma.ModelSchema):
 #   class Meta:
  #      model = Point
