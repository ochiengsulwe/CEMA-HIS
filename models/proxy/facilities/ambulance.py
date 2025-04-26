from api.v1 import db
from models.base_model import BaseModel


class ProxyAmbulance(BaseModel, db.Model):

    __tablename__ = 'proxy_ambulances'

    name = db.Column(db.String(124), nullable=False)
    registration_number = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(60), nullable=False)
    phone = db.Column(db.String(60), nullable=False)
