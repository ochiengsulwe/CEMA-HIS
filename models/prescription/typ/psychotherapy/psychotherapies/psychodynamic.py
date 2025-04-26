"""
A class of psycotherapy of psychodynamic
"""
from api.v1 import db
from models.base_model import BaseModel


class PsychoDynamicTherapy(BaseModel, db.Model):

    __tablename__ = 'psychodynamic_therapies'

    name = db.Column(db.String(60), nullable=False, unique=True)
    purpose = db.Column(db.String(60), nullable=False)
    delivery = db.Column(db.String(60), nullable=False)
    code = db.Column(db.String(60))
