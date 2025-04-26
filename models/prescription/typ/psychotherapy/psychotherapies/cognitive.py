"""
A class of psycotherapy of cognitive behavioral
"""
from api.v1 import db
from models.base_model import BaseModel


class CognitiveBehavioralTherapy(BaseModel, db.Model):

    __tablename__ = 'cognitive_behavioral_therapies'

    name = db.Column(db.String(60), nullable=False, unique=True)
    purpose = db.Column(db.String(60), nullable=False)
    delivery = db.Column(db.String(60), nullable=False)
    code = db.Column(db.String(60))
