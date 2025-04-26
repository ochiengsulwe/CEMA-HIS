"""
A class of medication Injected into muscle tissue (IM)
"""
from api.v1 import db
from models.base_model import BaseModel


class Intramuscular(BaseModel, db.Model):

    __tablename__ = 'intramusculars'

    name = db.Column(db.String(60), nullable=False, unique=True)
    frequency = db.Column(db.String(60), nullable=False)  # e.g "1, 2, 3"
    amounts = db.Column(db.String(60), nullable=False)  # e.g "50g, 100g, 500g,"
    code = db.Column(db.String(60))  # a unique code if available
    route = db.Column(db.String(60), nullable=False)
