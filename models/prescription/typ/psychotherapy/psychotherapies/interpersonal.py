"""
A class of psycotherapy of interpersonal
"""
from api.v1 import db
from models.base_model import BaseModel


class InterpersonalTherapy(BaseModel, db.Model):

    __tablename__ = 'interpersonal_therapies'

    name = db.Column(db.String(60), nullable=False, unique=True)
    purpose = db.Column(db.String(60), nullable=False)
    delivery = db.Column(db.String(60), nullable=False)
    code = db.Column(db.String(60))
