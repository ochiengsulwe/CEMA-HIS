from models.base_model import BaseModel
from api.v1 import db


class Physiotherapist(BaseModel, db.Model):

    __tablename__ = 'physiotherapists'

    id_num = db.Column(db.Integer, unique=True, index=True)
    first_name = db.Column(db.String(60))
    middle_name = db.Column(db.String(60))
    last_name = db.Column(db.String(60))
    gender = db.Column(db.Enum('Female', 'Male'), nullable=False)
    license_num = db.Column(db.String(60))
    reg_year = db.Column(db.Date)
    specialization = db.Column(db.String(64))
    spec_reg_num = db.Column(db.String(60))
    spec_year = db.Column(db.Date)
