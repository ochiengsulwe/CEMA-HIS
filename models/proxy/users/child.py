from models.base_model import BaseModel
from api.v1 import db


class Child(BaseModel, db.Model):

    __tablename__ = 'children'

    birth_cert_number = db.Column(db.Integer, unique=True, index=True)
    first_name = db.Column(db.String(60), nullable=False)
    middle_name = db.Column(db.String(60))
    gender = db.Column(db.Enum('Female', 'Male'), nullable=False)
    last_name = db.Column(db.String(60), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    facility_of_birth = db.Column(db.String(124))
    district_of_birth = db.Column(db.String(64))
    province_of_birth = db.Column(db.String(64))
    home_district = db.Column(db.String(64))
    home_division = db.Column(db.String(64))
    home_location = db.Column(db.String(64))
    home_sub_location = db.Column(db.String(64))
