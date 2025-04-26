from models.base_model import BaseModel
from api.v1 import db


class Citizen(BaseModel, db.Model):

    __tablename__ = 'citizens'

    id_num = db.Column(db.Integer, unique=True, index=True, nullable=False)
    first_name = db.Column(db.String(60), nullable=False)
    middle_name = db.Column(db.String(60))
    last_name = db.Column(db.String(60), nullable=False)
    gender = db.Column(db.Enum('Male', 'Female'), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    district_of_birth = db.Column(db.String(64))
    home_district = db.Column(db.String(64))
    home_division = db.Column(db.String(64))
    home_location = db.Column(db.String(64))
    home_sub_location = db.Column(db.String(64))
