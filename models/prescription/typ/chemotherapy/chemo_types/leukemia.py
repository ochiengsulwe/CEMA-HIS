"""
Leukemia Cancer Description
"""
from api.v1 import db
from models.base_model import BaseModel


class Leukemia(BaseModel, db.Model):

    __tablename__ = 'leukemias'

    name = db.Column(db.String(60), nullable=False, unique=True)
    intent = db.Column(db.String(60), nullable=False)
    cycle_type = db.Column(db.String(60), nullable=False)
    code = db.Column(db.String(60))  # a unique code if available
    delivery = db.Column(db.String(60), nullable=False)
