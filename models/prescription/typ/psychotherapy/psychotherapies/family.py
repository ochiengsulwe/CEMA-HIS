"""
A class of psycotherapy of family and group
"""
from api.v1 import db
from models.base_model import BaseModel


class FamilyGroupTherapy(BaseModel, db.Model):

    __tablename__ = 'family_group_therapies'

    name = db.Column(db.String(60), nullable=False, unique=True)
    purpose = db.Column(db.String(60), nullable=False)
    delivery = db.Column(db.String(60), nullable=False)
    code = db.Column(db.String(60))
