from datetime import datetime
from config import db

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(128), unique=True)
    description = db.Column(db.String(128))
    price = db.Column(db.Float, default=0)

class Rule(db.Model):
    __tablename__ = 'rules'
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(128))
    city = db.Column(db.String(128))
    sku = db.Column(db.String(128))
    min_condition = db.Column(db.Integer, default=0)
    max_condition = db.Column(db.Integer, default=0)
    variation = db.Column(db.Float, default=0)