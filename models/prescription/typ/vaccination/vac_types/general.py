"""
General vaccinations
"""
from api.v1 import db
from models.base_model import BaseModel


class GeneralVaccine(BaseModel, db.Model):

    __tablename__ = 'general_vaccines'

    name = db.Column(db.String(60), nullable=False, unique=True)
    frequency = db.Column(db.String(60), nullable=False)
    purpose = db.Column(db.String(60), nullable=False)
    code = db.Column(db.String(60))  # a unique code if available
    type = db.Column(db.String(60), nullable=False)
    delivery_strategy = db.Column(db.String(60), nullable=False)
