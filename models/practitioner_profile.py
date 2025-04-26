from api.v1 import db
from models.base_model import BaseModel


class PracProfile(BaseModel, db.Model):

    __tablename__ = 'prac_profiles'

    bio = db.Column(db.Text)
    fee = db.Column(db.Integer, nullable=False)  # Charge per consultation
    phone_number = db.Column(db.String(16), unique=True)
    profession_reg = db.Column(db.String(60), unique=True, nullable=False)
    prof_reg_year = db.Column(db.Date, nullable=False)
    profession = db.Column(db.String(64), nullable=False)
    specialization = db.Column(db.String(64))
    specialization_reg = db.Column(db.String(60), unique=True)
    spec_reg_year = db.Column(db.Date)
    loginfo_id = db.Column(db.String(60), db.ForeignKey('loginfos.id'))
    identity_id = db.Column(db.String(60), db.ForeignKey('users.id'))

    identity = db.relationship('User', back_populates='practitioner',
                               uselist=False)
    loginfo = db.relationship('LogInfo', back_populates='prac_profile',
                              uselist=False)
    appointments = db.relationship('Appointment', back_populates='practitioner')
    planner = db.relationship('Planner', back_populates='practitioner',
                              uselist=False)
    programs = db.relationship('PractitionerProgram', back_populates='practitioner',
                               cascade='all, delete-orphan')
