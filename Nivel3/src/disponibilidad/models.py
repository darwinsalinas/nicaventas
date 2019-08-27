from datetime import datetime
from config import db


class Country(db.Model):
    __tablename__ = 'countries'
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(128), unique=True)

class City(db.Model):
    __tablename__ = 'cities'
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(128))
    active = db.Column(db.Boolean)
    country_id = db.Column(db.Integer, db.ForeignKey('countries.id'))