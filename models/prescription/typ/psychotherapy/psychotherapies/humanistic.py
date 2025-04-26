"""
A class of psycotherapy of humanistic
"""
from api.v1 import db
from models.base_model import BaseModel


class HumanisticTherapy(BaseModel, db.Model):

    __tablename__ = 'humanistic_therapies'

    name = db.Column(db.String(60), nullable=False, unique=True)
    purpose = db.Column(db.String(60), nullable=False)
    delivery = db.Column(db.String(60), nullable=False)
    code = db.Column(db.String(60))
